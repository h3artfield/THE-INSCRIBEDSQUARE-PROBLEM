"""Intrinsic robust-square radius — mathematical definitions (no search dependence)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.robust_degree.perturbation_radius import E_gamma_B, squared_distance_perturbation_bound
from squarepeg.robust_degree.protected_box import ProtectedSquareBox, m_gamma_B
from squarepeg.robust_degree.square_map import CurveFn, curve_diameter

IntrinsicStatus = Literal[
    "positive_intrinsic",
    "zero_intrinsic",
    "not_evaluated",
]


@dataclass(frozen=True)
class IntrinsicRadiusDefinition:
    """
    Mathematical definition only.

    rho_square(gamma, B) = sup { eta > 0 :
      for all C^0 perturbations q with ||q - gamma||_infty <= eta on the four windows,
      (q, B) remains a protected square box with nonzero degree and vertex separation }.
    """

    description: str = (
        "Supremum eta such that all C^0 perturbations within eta on support windows "
        "preserve protected-box status (boundary exclusion, degree, separation, side length)."
    )


def intrinsic_rho_box(
    gamma: CurveFn,
    box: ProtectedSquareBox,
    *,
    boundary_margin: float,
    separation_margin: float,
) -> float:
    """
    Compute intrinsic rho from certified margins when (gamma, B) is known protected.

    When the box is protected with margin m and separation d_min, the homotopy
    argument gives intrinsic rho >= min(m/(16D), d_min/4) (same formula as certified
    lower bound but interpreted as valid for ALL perturbations, not just one certificate).
    """
    if boundary_margin <= 0 or separation_margin <= 0:
        return 0.0
    D = curve_diameter(gamma)
    eta_m = 0.9 * boundary_margin / (16.0 * D) if D > 0 else 0.0
    eta_sep = 0.24 * separation_margin
    return min(eta_m, eta_sep)


def intrinsic_rho_curve(
    gamma: CurveFn,
    boxes: list[ProtectedSquareBox],
    margins: list[float],
    separations: list[float],
) -> tuple[float, IntrinsicStatus]:
    """rho_square(gamma) = sup_B rho_square(gamma, B)."""
    best = 0.0
    for box, m, s in zip(boxes, margins, separations):
        r = intrinsic_rho_box(gamma, box, boundary_margin=m, separation_margin=s)
        best = max(best, r)
    if best > 0:
        return best, "positive_intrinsic"
    return 0.0, "zero_intrinsic"


def intrinsic_positive_iff_c0_protected(gamma: CurveFn, rho: float) -> bool:
    """rho_square(gamma) > 0 iff curve has a C^0-protected square box."""
    return rho > 0


def square_exists_without_positive_intrinsic() -> str:
    """Documented possibility: square may exist while rho_square(gamma) = 0."""
    return (
        "A curve may admit inscribed squares while every protected box has "
        "intrinsic radius zero (e.g. squares only at scales below any uniform C^0 margin)."
    )
