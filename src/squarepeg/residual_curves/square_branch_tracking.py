"""Track certified square branches on truncated double-spiral polygons."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from squarepeg.certificates.schema import SquareCertificate
from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import PolygonSolveResult, solve_polygon_full
from squarepeg.residual_curves.canonical import CanonicalDoubleSpiral
from squarepeg.residual_curves.truncated_spirals import rational_truncated_spiral


@dataclass
class SquareBranchRecord:
    turns: int
    side_length: float
    side_over_diameter: float
    edge_indices: tuple[int, int, int, int]
    edge_parameters: tuple[str, str, str, str]
    vertex_radii: tuple[float, float, float, float]
    min_vertex_radius: float
    polygon_hash: str


def _diameter(poly: PolygonCurve) -> float:
    return 2.0 * max(
        math.hypot(float(x), float(y)) for x, y in poly.vertices
    )


def _record_from_cert(poly: PolygonCurve, turns: int, cert: SquareCertificate) -> SquareBranchRecord:
    side_sq = float(Fraction(cert.side_length_squared))
    side = math.sqrt(side_sq)
    diam = _diameter(poly)
    radii = tuple(
        math.hypot(float(Fraction(x)), float(Fraction(y)))
        for x, y in cert.vertices
    )
    return SquareBranchRecord(
        turns=turns,
        side_length=side,
        side_over_diameter=side / diam if diam else 0.0,
        edge_indices=cert.edge_indices,
        edge_parameters=cert.edge_parameters,
        vertex_radii=radii,
        min_vertex_radius=min(radii),
        polygon_hash=cert.polygon_hash,
    )


def macroscopic_branch_filter(
    rec: SquareBranchRecord,
    *,
    min_side_ratio: float = 0.3,
    min_radius: float = 0.05,
) -> bool:
    return rec.side_over_diameter >= min_side_ratio and rec.min_vertex_radius >= min_radius


def analyze_truncation(turns: int, *, denom: int = 1000) -> list[SquareBranchRecord]:
    poly = rational_truncated_spiral(turns, denom=denom)
    if poly is None:
        return []
    result = solve_polygon_full(poly, allow_repeated_edges=True)
    return [_record_from_cert(poly, turns, c) for c in result.isolated]


def stable_outer_branch(
    turn_range: range | None = None,
    *,
    min_side_ratio: float = 0.45,
    min_radius: float = 0.15,
) -> list[SquareBranchRecord]:
    """Collect macroscopic squares stable across turn counts."""
    if turn_range is None:
        turn_range = range(3, 8)
    by_key: dict[tuple, list[SquareBranchRecord]] = {}
    for t in turn_range:
        for rec in analyze_truncation(t):
            if not macroscopic_branch_filter(
                rec, min_side_ratio=min_side_ratio, min_radius=min_radius
            ):
                continue
            key = (rec.edge_parameters[0], rec.edge_parameters[1], rec.edge_parameters[2])
            by_key.setdefault(key, []).append(rec)
    stable = []
    for recs in by_key.values():
        if len(recs) >= 2:
            stable.append(max(recs, key=lambda r: r.side_over_diameter))
    return sorted(stable, key=lambda r: -r.side_over_diameter)


def branch_continuation_report(turns_max: int = 7) -> dict[str, Any]:
    """Summary for directive report."""
    branches = stable_outer_branch(range(3, turns_max + 1))
    if not branches:
        return {"stable_count": 0}
    best = branches[0]
    per_turn = {t: analyze_truncation(t) for t in range(3, turns_max + 1)}
    return {
        "stable_count": len(branches),
        "best_side_over_diameter": best.side_over_diameter,
        "best_edge_indices": best.edge_indices,
        "best_parameters": best.edge_parameters,
        "best_radii": best.vertex_radii,
        "min_radius": best.min_vertex_radius,
        "side_lower_bound_observed": min(
            r.side_over_diameter
            for recs in per_turn.values()
            for r in recs
            if macroscopic_branch_filter(r, min_side_ratio=0.45, min_radius=0.15)
        )
        if any(per_turn.values())
        else None,
    }
