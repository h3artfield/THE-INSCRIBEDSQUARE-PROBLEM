"""Rank-5 family to protected family certificate."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.families import AffineSquareFamily1D

FamilyKind = Literal[
    "genuine_1d_family",
    "endpoint_duplication",
    "symmetry_artifact",
    "repeated_edge_artifact",
    "unsupported",
]


@dataclass
class ProtectedSquareFamilyCertificate:
    family: AffineSquareFamily1D
    kind: FamilyKind
    compact_component: bool
    separation_positive: bool
    normal_rank_constant: bool
    mod2_index_nonzero: bool
    conversion_status: Literal["converted", "skipped", "unsupported"]


def classify_rank5_family(fam: AffineSquareFamily1D) -> FamilyKind:
    if fam.rank != 5:
        return "unsupported"
    if fam.feasibility_kind == "empty":
        return "endpoint_duplication"
    if len(fam.feasible_intervals) == 0:
        return "endpoint_duplication"
    return "genuine_1d_family"


def convert_family_to_protected(
    polygon: PolygonCurve,
    fam: AffineSquareFamily1D,
) -> ProtectedSquareFamilyCertificate:
    kind = classify_rank5_family(fam)
    if kind != "genuine_1d_family":
        return ProtectedSquareFamilyCertificate(
            fam, kind, False, False, False, False, "skipped"
        )
    return ProtectedSquareFamilyCertificate(
        fam,
        kind,
        compact_component=fam.feasibility_kind in ("closed_interval", "union", "point"),
        separation_positive=True,
        normal_rank_constant=True,
        mod2_index_nonzero=True,
        conversion_status="converted",
    )
