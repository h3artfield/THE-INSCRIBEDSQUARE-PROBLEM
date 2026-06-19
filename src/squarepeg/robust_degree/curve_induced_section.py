"""Curve-induced obstruction sections s_h = pi_E(D_gamma F[h])."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np

from squarepeg.robust_degree.cokernel_bundle import cokernel_fiber_at, df_matrix
from squarepeg.robust_degree.square_family import circle_gamma, circle_square_family
from squarepeg.robust_degree.square_map import CurveFn, square_map_F

CurvePerturbation = Callable[[float], tuple[float, float]]


@dataclass
class CurveInducedSectionAudit:
    mean: float
    max_abs: float
    min_value: float
    max_value: float
    has_zero_crossing: bool
    can_remove_abstract_family: bool
    restriction_candidates: list[str]
    notes: list[str]


def linearized_map_variation(
    gamma: CurveFn,
    h: CurvePerturbation,
    u: tuple[float, float, float, float],
    *,
    eps: float = 1e-5,
) -> np.ndarray:
    """D_gamma F[h](u) via directional derivative of F under gamma + eps*h."""

    def gamma_eps(t: float, scale: float) -> tuple[float, float]:
        x, y = gamma(t)
        hx, hy = h(t)
        return (x + scale * hx, y + scale * hy)

    base = np.array(square_map_F(gamma, u), dtype=float)
    pert = np.array(square_map_F(lambda t: gamma_eps(t, eps), u), dtype=float)
    return (pert - base) / eps


def curve_induced_section(
    gamma: CurveFn,
    parametrization: Callable[[float], tuple[float, float, float, float]],
    h: CurvePerturbation,
    ts: np.ndarray,
) -> list[float]:
    values: list[float] = []
    for t in ts:
        u = parametrization(float(t))
        dF = linearized_map_variation(gamma, h, u)
        ell = cokernel_fiber_at(gamma, u).covector
        values.append(float(np.dot(ell, dF)))
    return values


def audit_curve_induced_circle(
    h: CurvePerturbation | None = None,
    n: int = 64,
) -> CurveInducedSectionAudit:
    gamma = circle_gamma
    fam = circle_square_family()
    if h is None:

        def h(t: float) -> tuple[float, float]:
            return (0.1 * math.cos(t), 0.1 * math.sin(t))

    ts = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    values = curve_induced_section(gamma, fam.parametrization, h, ts)
    mean = float(np.mean(values))
    has_cross = any(values[i] * values[j] <= 0 for i in range(len(values)) for j in range(i + 1, len(values)))

    return CurveInducedSectionAudit(
        mean=mean,
        max_abs=max(abs(v) for v in values),
        min_value=min(values),
        max_value=max(values),
        has_zero_crossing=has_cross,
        can_remove_abstract_family=False,
        restriction_candidates=[
            "curve-induced sections lie in im(D_gamma F), not all sections of E",
            "small symmetric radial bumps yield near-zero mean obstruction",
            "T038-Curve (CONJECTURAL): curve-induced sections always have a zero on circle family",
        ],
        notes=[
            "Abstract constant cokernel section removes circle family (Circle-B)",
            "Curve perturbations gamma -> gamma+h do not realize arbitrary sections",
        ],
    )


def t038_curve_statement() -> str:
    return (
        "T038-Curve (CONJECTURAL): For the unit-circle ordered square family, every "
        "sufficiently small curve-induced perturbation yields an obstruction section "
        "s_h : S^1 -> E with at least one zero. Mechanism: image(D_gamma F|_Z) does not "
        "contain a nowhere-vanishing cokernel section."
    )
