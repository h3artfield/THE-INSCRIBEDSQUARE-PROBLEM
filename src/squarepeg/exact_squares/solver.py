"""Exact square solver with affine-family representation (no sampling)."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal

from squarepeg.certificates.schema import SquareCertificate, square_dedup_key
from squarepeg.curves.polygon import Point, PolygonCurve
from squarepeg.exact_squares.equations import build_square_system
from squarepeg.exact_squares.families import (
    AffineSquareFamily1D,
    UnsupportedHigherDimensionalFamily,
    endpoint_values,
    solve_affine_system,
    x_at_t,
)

Rotation = Literal["ccw", "cw"]


@dataclass
class SquareSolution:
    edge_indices: tuple[int, int, int, int]
    parameters: tuple[Fraction, Fraction, Fraction, Fraction]
    side_vector: tuple[Fraction, Fraction]
    rotation: Rotation
    vertices: tuple[Point, Point, Point, Point]


@dataclass
class PolygonSolveResult:
    isolated: list[SquareCertificate] = field(default_factory=list)
    families_1d: list[AffineSquareFamily1D] = field(default_factory=list)
    unsupported: list[UnsupportedHigherDimensionalFamily] = field(default_factory=list)
    inconsistent_count: int = 0
    stats: dict = field(default_factory=dict)

    def all_certificates(self) -> list[SquareCertificate]:
        return list(self.isolated)

    def dedup_isolated(self) -> None:
        seen: dict[tuple, SquareCertificate] = {}
        for cert in self.isolated:
            key = cert.dedup_key()
            if key not in seen:
                seen[key] = cert
        self.isolated = list(seen.values())


def _vertices_from_params(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    params: tuple[Fraction, ...],
) -> tuple[Point, Point, Point, Point]:
    return (
        polygon.evaluate_edge(edges[0], params[0]),
        polygon.evaluate_edge(edges[1], params[1]),
        polygon.evaluate_edge(edges[2], params[2]),
        polygon.evaluate_edge(edges[3], params[3]),
    )


def _compute_residuals(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    params: Sequence[Fraction],
    side: Point,
    rotation: Rotation,
) -> dict[str, str]:
    from squarepeg.exact_squares.validator import build_equations_independent
    from squarepeg.exact_squares.families import residual_at

    matrix, rhs = build_equations_independent(polygon, edges, rotation)
    x = tuple(params) + tuple(side)
    res = residual_at(matrix, rhs, x)
    return {"system": str(res)}


def _diagonal_squared(vertices: tuple[Point, ...]) -> Fraction:
    p1, _, p3, _ = vertices
    dx = p1[0] - p3[0]
    dy = p1[1] - p3[1]
    return dx * dx + dy * dy


from typing import Sequence  # noqa: E402


def _solution_to_certificate(
    polygon: PolygonCurve, sol: SquareSolution
) -> SquareCertificate:
    side_sq = sol.side_vector[0] ** 2 + sol.side_vector[1] ** 2
    diag_sq = _diagonal_squared(sol.vertices)
    return SquareCertificate(
        polygon_hash=polygon.polygon_hash(),
        edge_indices=sol.edge_indices,
        edge_parameters=tuple(str(p) for p in sol.parameters),
        vertices=tuple((str(v[0]), str(v[1])) for v in sol.vertices),
        orientation=sol.rotation,
        side_length_squared=str(side_sq),
        diagonal_length_squared=str(diag_sq),
        residuals=_compute_residuals(
            polygon, sol.edge_indices, sol.parameters, sol.side_vector, sol.rotation
        ),
        cyclic_order_verified=True,
        certificate_type="exact",
        side_vector=(str(sol.side_vector[0]), str(sol.side_vector[1])),
    )


def _is_valid_isolated(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    x: tuple[Fraction, ...],
) -> bool:
    from squarepeg.exact_squares.validator import validate_geometry

    params = x[:4]
    side = (x[4], x[5])
    if any(p < 0 or p > 1 for p in params):
        return False
    if side[0] ** 2 + side[1] ** 2 == 0:
        return False
    return validate_geometry(polygon, edges, params).ok


def solve_edge_quadruple(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> tuple[list[SquareCertificate], list[AffineSquareFamily1D], list[UnsupportedHigherDimensionalFamily]]:
    """Solve one edge quadruple exactly; no sampling."""
    empty: tuple[list, list, list] = ([], [], [])
    if len(set(edges)) == 4 and not polygon.cyclic_order(*edges):
        return empty

    matrix, rhs = build_square_system(polygon, edges, rotation)
    solved = solve_affine_system(matrix, rhs)

    if solved.inconsistent:
        return empty

    isolated: list[SquareCertificate] = []
    families: list[AffineSquareFamily1D] = []
    unsupported: list[UnsupportedHigherDimensionalFamily] = []

    if solved.rank == 6 and solved.particular is not None:
        x = solved.particular
        if _is_valid_isolated(polygon, edges, x):
            params = x[:4]
            side = (x[4], x[5])
            sol = SquareSolution(
                edge_indices=edges,
                parameters=params,  # type: ignore[arg-type]
                side_vector=side,
                rotation=rotation,
                vertices=_vertices_from_params(polygon, edges, params),
            )
            isolated.append(_solution_to_certificate(polygon, sol))
        return isolated, families, unsupported

    if solved.rank == 5 and solved.particular and len(solved.nullspace) == 1:
        fam = AffineSquareFamily1D.build(polygon, edges, rotation, solved)
        families.append(fam)
        x0 = solved.particular
        d = solved.nullspace[0]
        from squarepeg.exact_squares.families import TInterval

        intervals = [
            TInterval(
                Fraction(iv["lo"]),
                Fraction(iv["hi"]),
                iv["lo_closed"],
                iv["hi_closed"],
            )
            for iv in fam.feasible_intervals
        ]
        for t in endpoint_values(intervals):
            x = x_at_t(x0, d, t)
            if _is_valid_isolated(polygon, edges, x):
                params = x[:4]
                side = (x[4], x[5])
                sol = SquareSolution(
                    edge_indices=edges,
                    parameters=params,  # type: ignore[arg-type]
                    side_vector=side,
                    rotation=rotation,
                    vertices=_vertices_from_params(polygon, edges, params),
                )
                cert = _solution_to_certificate(polygon, sol)
                key = cert.dedup_key()
                if not any(c.dedup_key() == key for c in isolated):
                    isolated.append(cert)
        return isolated, families, unsupported

    if solved.rank <= 4:
        unsupported.append(
            UnsupportedHigherDimensionalFamily.build(polygon, edges, rotation, solved)
        )
        return isolated, families, unsupported

    return empty


def solve_polygon_full(
    polygon: PolygonCurve,
    *,
    allow_repeated_edges: bool = True,
    distinct_edges_only: bool = False,
) -> PolygonSolveResult:
    import time

    polygon = polygon.normalize_orientation()
    allow_rep = allow_repeated_edges and not distinct_edges_only
    result = PolygonSolveResult()
    t0 = time.perf_counter()
    t_gen = t0
    t_mat = t0
    t_rank = t0
    quadruples = 0
    pruned = 0

    for edges in polygon.iter_cyclic_edge_quadruples(allow_repeated=allow_rep):
        if distinct_edges_only and len(set(edges)) < 4:
            pruned += 1
            continue
        quadruples += 1
        for rotation in ("ccw", "cw"):
            iso, fams, uns = solve_edge_quadruple(polygon, edges, rotation)
            result.isolated.extend(iso)
            result.families_1d.extend(fams)
            result.unsupported.extend(uns)

    result.dedup_isolated()
    t1 = time.perf_counter()
    result.stats = {
        "quadruples_examined": quadruples,
        "quadruples_pruned": pruned,
        "isolated_count": len(result.isolated),
        "families_1d_count": len(result.families_1d),
        "unsupported_count": len(result.unsupported),
        "runtime_seconds": t1 - t0,
    }
    return result


def solve_polygon(
    polygon: PolygonCurve,
    *,
    allow_repeated_edges: bool = True,
    distinct_edges_only: bool = False,
) -> list[SquareCertificate]:
    """Backward-compatible: return deduplicated isolated exact certificates."""
    return solve_polygon_full(
        polygon,
        allow_repeated_edges=allow_repeated_edges,
        distinct_edges_only=distinct_edges_only,
    ).isolated
