"""Independent square certificate validation (does not import solver assembly)."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal, Sequence

from squarepeg.certificates.schema import SquareCertificate
from squarepeg.curves.polygon import Point, PolygonCurve
from squarepeg.exact_squares.families import (
    AffineSquareFamily1D,
    AffineSquareFamilyND,
    UnsupportedHigherDimensionalFamily,
    residual_at,
    x_at_t,
)

Rotation = Literal["ccw", "cw"]


def _rotation_matrix(kind: Rotation) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    if kind == "ccw":
        return ((Fraction(0), Fraction(-1)), (Fraction(1), Fraction(0)))
    return ((Fraction(0), Fraction(1)), (Fraction(-1), Fraction(0)))


def build_equations_independent(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> tuple[list[list[Fraction]], list[Fraction]]:
    """Independent 6×6 assembly for validation (not imported from solver)."""
    j = _rotation_matrix(rotation)
    origins: list[Point] = []
    directions: list[Point] = []
    for idx in edges:
        o, d = polygon.edge_parametric(idx)
        origins.append(o)
        directions.append(d)

    rows: list[list[Fraction]] = []
    rhs: list[Fraction] = []

    for comp in range(2):
        row = [Fraction(0)] * 6
        row[0] = -directions[0][comp]
        row[1] = directions[1][comp]
        row[4 + comp] = Fraction(-1)
        rows.append(row)
        rhs.append(origins[0][comp] - origins[1][comp])

    ij = (
        (Fraction(1) + j[0][0], j[0][1]),
        (j[1][0], Fraction(1) + j[1][1]),
    )
    for comp in range(2):
        row = [Fraction(0)] * 6
        row[0] = -directions[0][comp]
        row[2] = directions[2][comp]
        row[4] = -ij[comp][0]
        row[5] = -ij[comp][1]
        rows.append(row)
        rhs.append(origins[0][comp] - origins[2][comp])

    for comp in range(2):
        row = [Fraction(0)] * 6
        row[0] = -directions[0][comp]
        row[3] = directions[3][comp]
        row[4] = -j[comp][0]
        row[5] = -j[comp][1]
        rows.append(row)
        rhs.append(origins[0][comp] - origins[3][comp])

    return rows, rhs


def reconstruct_vertices(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    params: Sequence[Fraction],
) -> tuple[Point, Point, Point, Point]:
    return (
        polygon.evaluate_edge(edges[0], params[0]),
        polygon.evaluate_edge(edges[1], params[1]),
        polygon.evaluate_edge(edges[2], params[2]),
        polygon.evaluate_edge(edges[3], params[3]),
    )


def _on_segment(p: Point, a: Point, b: Point) -> bool:
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    if cross != 0:
        return False
    dot1 = (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])
    dot2 = (p[0] - b[0]) * (a[0] - b[0]) + (p[1] - b[1]) * (a[1] - b[1])
    return dot1 >= 0 and dot2 >= 0


def _dist_sq(a: Point, b: Point) -> Fraction:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def _dot(a: Point, b: Point) -> Fraction:
    return a[0] * b[0] + a[1] * b[1]


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]


def validate_cyclic_order(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    params: Sequence[Fraction],
) -> bool:
    if len(set(edges)) == 4:
        return polygon.cyclic_order(*edges)
    tagged = list(zip(edges, params))
    prev_e, prev_u = tagged[0]
    n = polygon.num_edges
    for e, u in tagged[1:]:
        de = (e - prev_e) % n
        if de == 0 and u <= prev_u:
            return False
        prev_e, prev_u = e, u
    return True


def validate_geometry(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    params: Sequence[Fraction],
) -> ValidationResult:
    errors: list[str] = []
    if any(p < 0 or p > 1 for p in params):
        errors.append("edge parameter outside [0,1]")

    verts = reconstruct_vertices(polygon, edges, params)
    for i, (edge_i, p) in enumerate(zip(edges, verts)):
        a, b = polygon.edge(edge_i)
        if not _on_segment(p, a, b):
            errors.append(f"vertex {i} not on edge {edge_i}")

    if not validate_cyclic_order(polygon, edges, params):
        errors.append("cyclic boundary order violated")

    p1, p2, p3, p4 = verts
    if len({p1, p2, p3, p4}) < 4:
        errors.append("vertices not distinct")

    s1 = _dist_sq(p1, p2)
    s2 = _dist_sq(p2, p3)
    s3 = _dist_sq(p3, p4)
    s4 = _dist_sq(p4, p1)
    if min(s1, s2, s3, s4) == 0:
        errors.append("zero side length")
    elif not (s1 == s2 == s3 == s4):
        errors.append("side lengths not equal")

    d1 = _dist_sq(p1, p3)
    d2 = _dist_sq(p2, p4)
    if d1 != d2:
        errors.append("diagonals not equal")

    v12 = (p2[0] - p1[0], p2[1] - p1[1])
    v23 = (p3[0] - p2[0], p3[1] - p2[1])
    if _dot(v12, v23) != 0:
        errors.append("adjacent sides not perpendicular")

    return ValidationResult(ok=len(errors) == 0, errors=errors)


def validate_square_certificate(
    polygon: PolygonCurve, cert: SquareCertificate
) -> ValidationResult:
    errors: list[str] = []
    if cert.polygon_hash != polygon.polygon_hash():
        errors.append("polygon hash mismatch")
    if cert.certificate_type != "exact":
        errors.append(f"expected exact certificate, got {cert.certificate_type}")

    params = tuple(Fraction(p) for p in cert.edge_parameters)
    geom = validate_geometry(polygon, cert.edge_indices, params)
    errors.extend(geom.errors)

    # Independent equation check
    matrix, rhs = build_equations_independent(
        polygon, cert.edge_indices, cert.orientation
    )
    x = params + tuple(Fraction(v) for v in cert.side_vector)
    res = residual_at(matrix, rhs, x)
    if any(r != 0 for r in res):
        errors.append(f"equation residual nonzero: {res}")

    stored = tuple((Fraction(a), Fraction(b)) for a, b in cert.vertices)
    rebuilt = reconstruct_vertices(polygon, cert.edge_indices, params)
    if stored != rebuilt:
        errors.append("stored vertices differ from edge reconstruction")

    return ValidationResult(ok=len(errors) == 0, errors=errors)


def validate_affine_family_1d(
    polygon: PolygonCurve, family: AffineSquareFamily1D
) -> ValidationResult:
    errors: list[str] = []
    if family.polygon_hash != polygon.polygon_hash():
        errors.append("polygon hash mismatch")

    matrix = [[Fraction(c) for c in row] for row in family.matrix]
    rhs = [Fraction(b) for b in family.rhs]
    x0 = tuple(Fraction(v) for v in family.base_point)
    d = tuple(Fraction(v) for v in family.direction)

    if any(r != 0 for r in residual_at(matrix, rhs, x0)):
        errors.append("base point does not satisfy Ax=b")
    if any(r != 0 for r in residual_at(matrix, [Fraction(0)] * len(rhs), d)):
        errors.append("direction not in nullspace")

    # Symbolic: verify for one interior t if feasible
    from squarepeg.exact_squares.families import TInterval

    if family.feasibility_kind == "empty":
        return ValidationResult(ok=len(errors) == 0, errors=errors)

    for iv_dict in family.feasible_intervals:
        iv = TInterval(
            Fraction(iv_dict["lo"]),
            Fraction(iv_dict["hi"]),
            iv_dict["lo_closed"],
            iv_dict["hi_closed"],
        )
        if iv.is_empty():
            continue
        t = iv.lo if iv.lo_closed else iv.lo + Fraction(1, 1000)
        if not iv.contains(t):
            t = iv.hi if iv.hi_closed else iv.hi - Fraction(1, 1000)
        if abs(t) > Fraction(10**12):
            continue
        x = x_at_t(x0, d, t)
        if any(r != 0 for r in residual_at(matrix, rhs, x)):
            errors.append(f"family point at t={t} violates equations")
        params = x[:4]
        if family.feasibility_kind != "empty":
            g = validate_geometry(polygon, family.edge_indices, params)
            if not g.ok and family.feasibility_kind not in ("empty",):
                errors.append(f"geometry at sample t={t}: {g.errors}")

    for t_str in family.endpoint_isolated_t:
        t = Fraction(t_str)
        if abs(t) > Fraction(10**12):
            continue
        x = x_at_t(x0, d, t)
        params = x[:4]
        if any(p < 0 or p > 1 for p in params):
            continue
        g = validate_geometry(polygon, family.edge_indices, params)
        if not g.ok:
            errors.append(f"endpoint t={t} geometry: {g.errors}")

    return ValidationResult(ok=len(errors) == 0, errors=errors)


def validate_unsupported_family(
    polygon: PolygonCurve, uns: UnsupportedHigherDimensionalFamily
) -> ValidationResult:
    errors: list[str] = []
    if uns.polygon_hash != polygon.polygon_hash():
        errors.append("polygon hash mismatch")
    if uns.nullspace_dimension < 2:
        errors.append("expected nullspace dimension >= 2")
    nd = uns.nd_family
    matrix = [[Fraction(c) for c in row] for row in nd.matrix]
    rhs = [Fraction(b) for b in nd.rhs]
    x0 = tuple(Fraction(v) for v in nd.base_point)
    if any(r != 0 for r in residual_at(matrix, rhs, x0)):
        errors.append("particular solution residual nonzero")
    return ValidationResult(ok=len(errors) == 0, errors=errors)
