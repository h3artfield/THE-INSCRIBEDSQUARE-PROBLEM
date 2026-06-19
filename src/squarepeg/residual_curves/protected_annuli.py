"""Protected annuli for double-spiral winding certificates."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.residual_curves.canonical import CANONICAL_EPS_FLOAT, CANONICAL_THETA0
from squarepeg.residual_curves.double_spiral import d_separation, gamma_minus, gamma_plus, r_outer

from squarepeg.residual_curves.annular_winding import Annulus


@dataclass(frozen=True)
class ProtectedAnnulus:
    """Annulus A_j with inner protected subannulus A_j'."""

    index: int
    theta_center: float
    outer: Annulus
    protected: Annulus
    min_arm_separation: float
    min_distance_to_origin: float


def _turn_theta(j: int, theta0: float = CANONICAL_THETA0) -> float:
    """Center angle of half-turn j (0-indexed from outer)."""
    return theta0 + j * math.pi / 2.0 + math.pi / 4.0


def annulus_for_turn(
    j: int,
    *,
    theta0: float = CANONICAL_THETA0,
    eps: float = CANONICAL_EPS_FLOAT,
    width_factor: float = 0.35,
) -> ProtectedAnnulus:
    """
    Build disjoint annulus around half-turn j of the outer arm.

    Radial bounds use r(theta) at quarter-turn offsets; protected subannulus
    is a fixed fraction of the width.
    """
    th = _turn_theta(j, theta0)
    r_in = r_outer(th + math.pi / 4.0)
    r_out = r_outer(th - math.pi / 4.0)
    a_j = min(r_in, r_out) * 0.98
    b_j = max(r_in, r_out) * 1.02
    width = b_j - a_j
    a_p = a_j + width * (1.0 - width_factor) / 2.0
    b_p = b_j - width * (1.0 - width_factor) / 2.0
    rp = gamma_plus(th)
    rm = gamma_minus(th, eps)
    sep = math.hypot(rp[0] - rm[0], rp[1] - rm[1])
    return ProtectedAnnulus(
        index=j,
        theta_center=th,
        outer=Annulus(a_j, b_j),
        protected=Annulus(a_p, b_p),
        min_arm_separation=sep,
        min_distance_to_origin=a_j,
    )


def protected_annuli_for_turns(
    turn_count: int,
    *,
    theta0: float = CANONICAL_THETA0,
    eps: float = CANONICAL_EPS_FLOAT,
    even_only: bool = True,
) -> list[ProtectedAnnulus]:
    indices = range(0, turn_count, 2) if even_only else range(turn_count)
    return [annulus_for_turn(j, theta0=theta0, eps=eps) for j in indices]


def annuli_pairwise_disjoint(annuli: list[ProtectedAnnulus]) -> bool:
    for i in range(len(annuli)):
        for j in range(i + 1, len(annuli)):
            a, b = annuli[i].outer, annuli[j].outer
            if not (a.outer <= b.inner or b.outer <= a.inner):
                return False
    return True


def min_approximation_tolerance(ann: ProtectedAnnulus) -> float:
    """
    Hausdorff tolerance below which a subarc cannot change winding in A_j'
    without crossing the annulus boundary (half the protected radial width).
    """
    return 0.25 * (ann.protected.outer - ann.protected.inner)


def area_contribution_lower_bound(ann: ProtectedAnnulus, winding: int = 1) -> float:
    """Signed area lower bound from one full positive winding in protected annulus."""
    p = ann.protected
    return abs(winding) * math.pi * (p.outer**2 - p.inner**2) / 2.0
