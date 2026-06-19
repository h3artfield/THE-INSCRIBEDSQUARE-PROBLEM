"""Generalized intrinsic and certified robust radius."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.robust_degree.certified_lower_bound import underline_rho_k
from squarepeg.robust_degree.family_certificate import convert_family_to_protected
from squarepeg.robust_degree.polygon_extractor import convert_isolated_square
from squarepeg.robust_degree.protected_box import ProtectedSquareBox

SearchInterpretation = Literal[
    "ISOLATED_CERTIFICATE_FOUND",
    "FAMILY_CERTIFICATE_FOUND",
    "NO_CERTIFICATE_AT_LEVEL_K",
    "UNSUPPORTED_COMPONENT",
    "PROVED_NO_PROTECTED_COMPONENT",
]


@dataclass
class GeneralizedRadiusReport:
    underline_rho_k_gen: float
    isolated_contribution: float
    family_contribution: float
    level: int
    interpretation: SearchInterpretation
    messages: list[str] = field(default_factory=list)


def underline_rho_k_generalized(
    polygon: PolygonCurve,
    level: int = 0,
    *,
    param_radius: float = 0.05,
) -> GeneralizedRadiusReport:
    """
    underline_rho_k^{gen}(P) = max(isolated box certs, family certs).

    Never equates NO_CERTIFICATE with mathematical zero.
    """
    result = solve_polygon_full(polygon)
    iso_best = 0.0
    fam_best = 0.0
    msgs: list[str] = []
    interp: SearchInterpretation = "NO_CERTIFICATE_AT_LEVEL_K"

    for cert in result.isolated:
        conv = convert_isolated_square(polygon, cert, param_radius=param_radius)
        if conv.conversion_status == "converted":
            iso_best = max(iso_best, conv.rho_certified_lower_bound)
            interp = "ISOLATED_CERTIFICATE_FOUND"

    for fam in result.families_1d:
        pf = convert_family_to_protected(polygon, fam)
        if pf.conversion_status == "converted":
            fam_best = max(fam_best, param_radius * 0.5)
            interp = "FAMILY_CERTIFICATE_FOUND"

    if result.unsupported:
        msgs.append(f"unsupported rank systems: {len(result.unsupported)}")

    total = max(iso_best, fam_best)
    return GeneralizedRadiusReport(
        underline_rho_k_gen=total,
        isolated_contribution=iso_best,
        family_contribution=fam_best,
        level=level,
        interpretation=interp if total > 0 else "NO_CERTIFICATE_AT_LEVEL_K",
        messages=msgs,
    )


def rho_square_gen_intrinsic_definition() -> str:
    return (
        "DEPRECATED for family components (Directive 017): use rho_square^obs. "
        "rho_square^{gen} included families with unproved normal-index persistence."
    )


def t032_dagger_statement() -> str:
    return (
        "T032-dagger (CONJECTURAL): intrinsic generalized collapse => area-tight subsequence. "
        "Strictly stronger than T032* when families contribute (e.g. circle)."
    )
