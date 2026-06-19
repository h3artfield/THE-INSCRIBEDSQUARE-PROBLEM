"""Certified lower bounds rho_k and rho_infty — distinct from intrinsic rho."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal

from squarepeg.robust_degree.perturbation_radius import (
    E_gamma_B,
    rho_square_box,
)
from squarepeg.robust_degree.protected_box import ProtectedSquareBox
from squarepeg.robust_degree.square_map import CurveFn

SearchResult = Literal[
    "CERTIFIED_POSITIVE",
    "NOT_FOUND_AT_LEVEL_K",
    "UNSUPPORTED_DEGREE_CASE",
    "NO_PROTECTED_BOX_AT_LEVEL",
]

CertifiedStatus = Literal[
    "certified_positive",
    "zero_by_certificate",
    "not_certified",
    "no_protected_box",
]


def rho_square_certified_lower_bound_box(
    gamma: CurveFn,
    box: ProtectedSquareBox,
    *,
    boundary_margin: float | None = None,
) -> tuple[float, CertifiedStatus]:
    """
    Certified lower bound on intrinsic rho_square(gamma, B) from one certificate.

    Renamed from rho_square_box — this is NOT the intrinsic invariant.
    """
    return rho_square_box(gamma, box, boundary_margin=boundary_margin)


# Backward-compatible alias (deprecated)
rho_square_box_certified = rho_square_certified_lower_bound_box


def underline_rho_k(
    gamma: CurveFn,
    boxes_at_level_k: list[ProtectedSquareBox],
    *,
    boundary_margins: list[float] | None = None,
    level: int = 0,
) -> float:
    """
    underline_rho_k(P) = max certified radius over boxes of complexity <= k at search level k.
    """
    margins = boundary_margins or [None] * len(boxes_at_level_k)  # type: ignore[list-item]
    best = 0.0
    for box, m in zip(boxes_at_level_k, margins):
        r, status = rho_square_certified_lower_bound_box(gamma, box, boundary_margin=m)
        if status == "certified_positive":
            best = max(best, r)
    return best


def underline_rho_infinity(sequence: list[float]) -> float:
    """underline_rho_infty = sup_k underline_rho_k — monotone in k."""
    return max(sequence) if sequence else 0.0


def monotonicity_underline_rho(rho_k_values: list[float]) -> bool:
    """Verify 0 <= rho_k <= rho_{k+1} <= rho_square (when computed on nested search)."""
    for i in range(len(rho_k_values) - 1):
        if rho_k_values[i] > rho_k_values[i + 1] + 1e-15:
            return False
    return True


@dataclass
class CertifiedLowerBoundRecord:
    level: int
    underline_rho_k: float
    result: SearchResult
    boxes_examined: int = 0
    messages: list[str] = field(default_factory=list)


def never_return_zero_without_proof(result: SearchResult) -> bool:
    """Finite search must not claim intrinsic zero."""
    return result in (
        "NOT_FOUND_AT_LEVEL_K",
        "UNSUPPORTED_DEGREE_CASE",
        "NO_PROTECTED_BOX_AT_LEVEL",
    )
