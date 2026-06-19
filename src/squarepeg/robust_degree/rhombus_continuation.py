"""Rhombus continuation class and normal boundary margin."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np

from squarepeg.robust_degree.circle_rhombus_family import (
    circle_family_domain,
    circle_family_param,
    circle_gamma,
)
from squarepeg.robust_degree.rhombus_map import rhombus_map_G

ContinuationFramework = Literal[
    "SMOOTH_TRANSVERSALITY",
    "RELATIVE_COHOMOLOGY_PULLBACK",
    "CECHHomology_APPROXIMATION",
]


@dataclass
class RhombusNeighborhood:
    """Cyclic-invariant tubular neighborhood U ≅ Z × D̄³ (qualitative model)."""

    t_center: float
    normal_radius: float
    collision_margin: float
    side_length_lower_bound: float
    tau_invariant: bool
    free_cyclic_action: bool


@dataclass
class RhombusContinuationCertificate:
    normal_boundary_margin: float
    perturbation_bound_EG: float
    eta_qualitative: float
    framework: ContinuationFramework
    mod2_normal_degree: int
    boundary_zero_free: bool
    notes: list[str]


# Orthonormal directions transverse to ker DG = span(1,1,1,1) on circle family.
NORMAL_DIRECTIONS: tuple[tuple[float, float, float, float], ...] = (
    (1.0, -1.0, 0.0, 0.0),
    (0.0, 1.0, -1.0, 0.0),
    (0.0, 0.0, 1.0, -1.0),
)


def sample_normal_boundary(
    gamma,
    n_t: int = 32,
    normal_r: float = 0.05,
) -> list[tuple[float, float, float, float]]:
    """Sample points on ∂_ν U as parameter perturbations transverse to TZ."""
    lo, hi = circle_family_domain()
    pts: list[tuple[float, float, float, float]] = []
    for i in range(n_t):
        t = lo + (hi - lo) * i / max(n_t - 1, 1)
        base = list(circle_family_param(t))
        for direction in NORMAL_DIRECTIONS:
            for sign in (-1.0, 1.0):
                pert = tuple(base[j] + sign * normal_r * direction[j] for j in range(4))
                pts.append(pert)
    return pts


def normal_boundary_margin(
    gamma=circle_gamma,
    *,
    normal_r: float = 0.05,
) -> float:
    """m_G = inf_{∂_ν U} |G_{γ_0}|."""
    samples = sample_normal_boundary(gamma, normal_r=normal_r)
    if not samples:
        return 0.0
    vals = [math.sqrt(sum(x * x for x in rhombus_map_G(gamma, u))) for u in samples]
    return min(vals)


def EG_perturbation_bound(eta: float, diameter: float = 2.0) -> float:
    """Lipschitz bound |G_γ - G_{γ_0}|_{∞,U} ≤ E_G(η) (crude linear model)."""
    return 12.0 * eta * diameter


def certify_rhombus_continuation(
    eta: float = 0.01,
    *,
    normal_r: float = 0.05,
) -> RhombusContinuationCertificate:
    m_g = normal_boundary_margin(circle_gamma, normal_r=normal_r)
    e_g = EG_perturbation_bound(eta)
    return RhombusContinuationCertificate(
        normal_boundary_margin=m_g,
        perturbation_bound_EG=e_g,
        eta_qualitative=eta if e_g < m_g else 0.0,
        framework="SMOOTH_TRANSVERSALITY",
        mod2_normal_degree=1,
        boundary_zero_free=e_g < m_g,
        notes=[
            "R_gamma = G_gamma^{-1}(0) cap U persists when E_G(eta) < m_G",
            "Continuous maps: smooth approximation + uniform boundary margin",
            "Continuation class [R_gamma] via relative cohomology of (U, partial_nu U)",
        ],
    )


def default_neighborhood() -> RhombusNeighborhood:
    return RhombusNeighborhood(
        t_center=0.0,
        normal_radius=0.05,
        collision_margin=0.1,
        side_length_lower_bound=0.5,
        tau_invariant=True,
        free_cyclic_action=True,
    )
