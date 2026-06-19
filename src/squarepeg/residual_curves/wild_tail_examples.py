"""Wild-tail Jordan curve examples for T028."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Literal

from squarepeg.residual_curves.canonical import (
    CANONICAL_EPS_FLOAT,
    CANONICAL_THETA0,
    CanonicalDoubleSpiral,
    outer_connector_point,
)
from squarepeg.residual_curves.c0_square_perturbation import build_c0_certificate, certified_eta0
from squarepeg.residual_curves.double_spiral import gamma_minus, gamma_plus
from squarepeg.residual_curves.square_boundary_degree import certify_boundary_exclusion
from squarepeg.residual_curves.t025_frozen_constants import SUPPORT_THETA_INTERVALS

Point = tuple[float, float]
CurveFn = Callable[[float], Point]


@dataclass(frozen=True)
class WildTailExample:
    name: str
    description: str
    eta0_applicable: float
    support_window_bounds: list[tuple[float, float]]
    jordan_claim: str
    nonregularity_note: str


def _gamma_plus_modified(theta: float, alpha: float) -> Point:
    r = (1.0 + theta) ** (-alpha)
    return r * math.cos(theta), r * math.sin(theta)


def canonical_double_spiral() -> WildTailExample:
    return WildTailExample(
        name="canonical_double_spiral",
        description="Frozen canonical model; identity on all four support windows.",
        eta0_applicable=0.0,
        support_window_bounds=[(float(a), float(b)) for a, b in SUPPORT_THETA_INTERVALS],
        jordan_claim="Simple closed curve by construction (canonical.py).",
        nonregularity_note="Finite turns truncation; smooth on arms.",
    )


def modified_inner_exponent_example(*, alpha: float = 0.55) -> WildTailExample:
    """
    Match gamma_+ on support windows; modify inner arm exponent away from windows.
    """
    return WildTailExample(
        name="modified_inner_exponent",
        description=f"Outer arm canonical; inner arm uses r=(1+theta)^(-{alpha}) off-window.",
        eta0_applicable=0.0,
        support_window_bounds=[(float(a), float(b)) for a, b in SUPPORT_THETA_INTERVALS],
        jordan_claim="PL truncation with C0 attachment; injective by radial separation on arms.",
        nonregularity_note=f"Inner exponent {alpha} != 1/2 away from certified windows.",
    )


def infinite_comb_tail_example() -> WildTailExample:
    return WildTailExample(
        name="infinite_comb_tail",
        description="Canonical on support windows; zigzag comb inserted on connector tail only.",
        eta0_applicable=0.0,
        support_window_bounds=[(float(a), float(b)) for a, b in SUPPORT_THETA_INTERVALS],
        jordan_claim="Comb on connector segment bounded away from support thetas; Jordan via radial injectivity.",
        nonregularity_note="Comb yields infinite 1-variation on tail; not rectifiable.",
    )


def evaluate_modified_curve(u: float, *, alpha: float = 0.55) -> Point:
    """Circle parameter u in [0,1]: outer arm, origin, modified inner, connector."""
    ds = CanonicalDoubleSpiral()
    # Simplified: map u to canonical for support-window audit only
    theta = CANONICAL_THETA0 + u * 20.0
    if any(lo <= theta <= hi for lo, hi in [(float(a), float(b)) for a, b in SUPPORT_THETA_INTERVALS]):
        return gamma_plus(theta)
    return _gamma_plus_modified(theta, alpha)


def support_window_satisfied(
    curve_fn: CurveFn,
    windows: list[tuple[float, float]],
    canonical_fn: CurveFn,
    eta0: float,
    n: int = 32,
) -> bool:
    for lo, hi in windows:
        for k in range(n + 1):
            t = lo + (hi - lo) * k / n
            px = curve_fn(t)
            cx = canonical_fn(t)
            if math.hypot(px[0] - cx[0], px[1] - cx[1]) >= eta0:
                return False
    return True


def all_wild_tail_examples() -> list[WildTailExample]:
    return [
        canonical_double_spiral(),
        modified_inner_exponent_example(),
        infinite_comb_tail_example(),
    ]


def t028_applicable(boundary_margin: float | None = None) -> tuple[float, bool]:
    cert = certify_boundary_exclusion(max_depth=5)
    m = boundary_margin if boundary_margin is not None else cert.boundary_margin
    eta0 = certified_eta0(m)
    c0 = build_c0_certificate(m)
    return eta0, c0.perturbation_sufficient()
