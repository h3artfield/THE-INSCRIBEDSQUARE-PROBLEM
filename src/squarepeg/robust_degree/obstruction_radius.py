"""Obstruction-protected robust radius rho_square^obs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.robust_degree.polygon_extractor import convert_isolated_square
from squarepeg.robust_degree.valid_family_certificate import (
    ProtectedSquareFamilyCertificateV2,
    reject_rank5_without_obstruction,
)

ComponentClass = Literal[
    "ISOLATED_BROUWER",
    "OBSTRUCTION_BUNDLE",
    "CURVE_RESTRICTED",
    "INADMISSIBLE",
]


@dataclass
class ObstructionRadiusReport:
    rho_square_obs: float
    isolated_contribution: float
    family_contribution: float
    admissible_components: list[ComponentClass]
    rejected_rank5_families: int
    messages: list[str] = field(default_factory=list)


def rho_square_obs_polygon(
    polygon: PolygonCurve,
    *,
    param_radius: float = 0.05,
) -> ObstructionRadiusReport:
    """
    rho_square^obs(gamma) = sup persistence radii over admissible protected components.

    Replaces provisional rho_square^gen; excludes normal-index-only families.
    """
    result = solve_polygon_full(polygon)
    iso_best = 0.0
    fam_best = 0.0
    rejected = 0
    admissible: list[ComponentClass] = []
    msgs: list[str] = []

    for cert in result.isolated:
        conv = convert_isolated_square(polygon, cert, param_radius=param_radius)
        if conv.conversion_status == "converted":
            iso_best = max(iso_best, conv.rho_certified_lower_bound)
            admissible.append("ISOLATED_BROUWER")

    for fam in result.families_1d:
        v2: ProtectedSquareFamilyCertificateV2 = reject_rank5_without_obstruction(fam)
        if v2.admissibility == "REJECTED_RANK_ONLY":
            rejected += 1
            admissible.append("INADMISSIBLE")
            msgs.extend(v2.messages[:1])

    total = iso_best  # families excluded until Euler obstruction proved
    return ObstructionRadiusReport(
        rho_square_obs=total,
        isolated_contribution=iso_best,
        family_contribution=fam_best,
        admissible_components=admissible,
        rejected_rank5_families=rejected,
        messages=msgs,
    )


def rho_square_obs_definition() -> str:
    return (
        "rho_square^obs(gamma) = sup persistence radii over admissible protected components: "
        "isolated Brouwer degree, Morse-Bott w_d(E)!=0, or proved curve-restricted obstruction."
    )


def t032_double_dagger_statement() -> str:
    return (
        "T032-double-dagger (CONJECTURAL_FULL_BRIDGE): If every compatible obstruction-protected "
        "square component along a polygonal sequence has radius tending to zero, then an "
        "area-tight subsequence exists. Replaces T032-dagger when family persistence unproved."
    )
