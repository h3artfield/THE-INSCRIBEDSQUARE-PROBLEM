"""Recursive defect candidate and normalized blow-up scaling."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence

Point = tuple[float, float]


@dataclass
class NormalizedBlowUp:
    r_k: float
    z_k: Point
    normalized_diameter: float
    normalized_area: float
    absolute_robust_radius_order: float
    notes: list[str] = field(default_factory=list)


@dataclass
class RecursiveDefectCandidate:
    """
    Candidate counterexample to T032* (not square-peg conjecture).

    Scaled spiral/comb packets in shrinking parameter intervals.
    """

    name: str
    description: str
    area_tight: bool
    intrinsic_rho_tends_to_zero: bool
    only_scale_shrinking_squares: bool
    jordan: bool
    status: str = "CANDIDATE_NOT_VERIFIED"


def normalized_blow_up(
    points: Sequence[Point],
    *,
    z_k: Point | None = None,
) -> NormalizedBlowUp:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    r_k = max(
        max(xs) - min(xs) if xs else 0.0,
        max(ys) - min(ys) if ys else 0.0,
        1e-12,
    )
    cx = sum(xs) / len(xs) if xs else 0.0
    cy = sum(ys) / len(ys) if ys else 0.0
    z = z_k or (cx, cy)
    scaled = [((p[0] - z[0]) / r_k, (p[1] - z[1]) / r_k) for p in points]
    from squarepeg.area_variation.signed_area import relative_area_increment

    norm_area = abs(relative_area_increment(scaled)) if len(scaled) >= 2 else 0.0
    return NormalizedBlowUp(
        r_k=r_k,
        z_k=z,
        normalized_diameter=1.0,
        normalized_area=norm_area,
        absolute_robust_radius_order=0.0,  # c * r_k -> 0
        notes=[
            "Protected square of normalized radius c>0 implies absolute radius O(r_k)->0.",
            "Blow-up square does NOT directly yield limit square on gamma.",
        ],
    )


def absolute_vs_normalized_robustness(c_normalized: float, r_k: float) -> float:
    """Absolute robust radius ~ c * r_k when blow-up has protected box at scale c."""
    return c_normalized * r_k


def recursive_spiral_comb_candidate() -> RecursiveDefectCandidate:
    return RecursiveDefectCandidate(
        name="recursive_spiral_comb_packets",
        description=(
            "Insert scaled high-winding comb/spiral packets in intervals of length 2^{-k}. "
            "Target: no area-tight PL subsequence; intrinsic rho->0; squares only at shrinking scales."
        ),
        area_tight=False,
        intrinsic_rho_tends_to_zero=False,
        only_scale_shrinking_squares=True,
        jordan=False,
        status="CANDIDATE_NOT_VERIFIED",
    )


def t036_controlled_defect_tree_hypothesis() -> str:
    return (
        "T036 (controlled class): If defect intervals form a tree of bounded width "
        "with separated nested annuli, then no area-tight subsequence implies "
        "positive intrinsic protected degree at fixed spatial scale."
    )
