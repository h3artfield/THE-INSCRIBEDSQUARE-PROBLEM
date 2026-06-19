"""Staged exhaustive search for protected boxes on rational polygons."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal

from squarepeg.certificates.schema import SquareCertificate
from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.robust_degree.certified_lower_bound import (
    CertifiedLowerBoundRecord,
    SearchResult,
    underline_rho_k,
)
from squarepeg.robust_degree.polygon_extractor import convert_isolated_square
from squarepeg.robust_degree.protected_box import ProtectedSquareBox


@dataclass
class ExhaustiveSearchConfig:
    max_level: int = 4
    param_radii: tuple[float, ...] = (0.02, 0.05, 0.1, 0.15)
    subdivision_depth: int = 2


@dataclass
class ExhaustiveSearchReport:
    polygon_hash: str
    levels: list[CertifiedLowerBoundRecord] = field(default_factory=list)
    underline_rho_infty: float = 0.0
    final_result: SearchResult = "NOT_FOUND_AT_LEVEL_K"
    never_claims_intrinsic_zero: bool = True


def _polygon_gamma(polygon: PolygonCurve, edges: tuple[int, int, int, int]):
    def gamma(theta: float) -> tuple[float, float]:
        i = min(3, max(0, int(theta)))
        t = theta - i
        p = polygon.evaluate_edge(edges[i], Fraction(t).limit_denominator(10**6))
        return float(p[0]), float(p[1])

    return gamma


def search_level_k(
    polygon: PolygonCurve,
    level: int,
    config: ExhaustiveSearchConfig,
) -> CertifiedLowerBoundRecord:
    """One search level: all isolated rank-6 squares with param radius from config."""
    radius = config.param_radii[min(level, len(config.param_radii) - 1)]
    result = solve_polygon_full(polygon)
    boxes: list[ProtectedSquareBox] = []
    margins: list[float] = []
    unsupported = len(result.families_1d) + len(result.unsupported)
    if unsupported > 0 and not result.isolated:
        return CertifiedLowerBoundRecord(
            level=level,
            underline_rho_k=0.0,
            result="UNSUPPORTED_DEGREE_CASE",
            messages=["rank-5 families or unsupported systems only"],
        )
    for cert in result.isolated:
        conv = convert_isolated_square(polygon, cert, param_radius=radius)
        if conv.conversion_status == "converted":
            boxes.append(conv.protected_box)
            margins.append(conv.protected_box.boundary_margin)
    if not boxes:
        return CertifiedLowerBoundRecord(
            level=level,
            underline_rho_k=0.0,
            result="NO_PROTECTED_BOX_AT_LEVEL",
            boxes_examined=len(result.isolated),
        )
    # Use first box gamma for rho (same polygon)
    cert0 = result.isolated[0]
    gamma = _polygon_gamma(polygon, cert0.edge_indices)
    rho = underline_rho_k(gamma, boxes, boundary_margins=margins, level=level)
    return CertifiedLowerBoundRecord(
        level=level,
        underline_rho_k=rho,
        result="CERTIFIED_POSITIVE" if rho > 0 else "NOT_FOUND_AT_LEVEL_K",
        boxes_examined=len(boxes),
    )


def exhaustive_polygon_search(
    polygon: PolygonCurve,
    config: ExhaustiveSearchConfig | None = None,
) -> ExhaustiveSearchReport:
    """Deterministic staged search — never returns intrinsic ZERO."""
    cfg = config or ExhaustiveSearchConfig()
    report = ExhaustiveSearchReport(polygon_hash=polygon.polygon_hash())
    rhos: list[float] = []
    for k in range(cfg.max_level + 1):
        rec = search_level_k(polygon, k, cfg)
        report.levels.append(rec)
        rhos.append(rec.underline_rho_k)
    report.underline_rho_infty = max(rhos) if rhos else 0.0
    if report.underline_rho_infty > 0:
        report.final_result = "CERTIFIED_POSITIVE"
    else:
        report.final_result = report.levels[-1].result if report.levels else "NOT_FOUND_AT_LEVEL_K"
    return report


# rho_square_certified_lower_bound_polygon lives in polygon_extractor
