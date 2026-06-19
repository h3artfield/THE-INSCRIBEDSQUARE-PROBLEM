"""Truncation geometry and certificate audit (Directive 011R)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from squarepeg.certificates.schema import SquareCertificate
from squarepeg.curves.polygon import PolygonCurve, Point
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.exact_squares.validator import validate_geometry
from squarepeg.residual_curves.canonical import CANONICAL_THETA0, CanonicalDoubleSpiral
from squarepeg.residual_curves.double_spiral import gamma_plus, r_outer
from squarepeg.residual_curves.truncated_spirals import rational_truncated_spiral

EdgeKind = Literal[
    "outer_arm",
    "origin_to_inner",
    "inner_arm",
    "inner_to_p_minus",
    "outer_connector",
    "unknown",
]


@dataclass(frozen=True)
class EdgeDescriptor:
    index: int
    kind: EdgeKind
    theta_lo: float | None
    theta_hi: float | None
    is_artificial: bool
    description: str


@dataclass(frozen=True)
class MacroSquareCertificate:
    turns: int
    edge_indices: tuple[int, int, int, int]
    edge_parameters: tuple[str, str, str, str]
    vertices: tuple[tuple[str, str], ...]
    side_length_squared: str
    solve_rank: int | None
    validator_ok: bool
    edge_descriptors: tuple[EdgeDescriptor, ...]


# Literal identical macro branch (0,3,5,0) discovered in audit.
MACRO_BRANCH_EDGES = (0, 3, 5, 0)
MACRO_BRANCH_PARAMS = (
    "123574909883123382656/783176785809004249471",
    "515566058505096737446/2349530357427012748413",
    "700507479376466581385/783176785809004249471",
    "711993239270205241846/783176785809004249471",
)


def vertex_count(turns: int) -> int:
    """Vertices in closed polygon with connector: 4N+5."""
    return 4 * turns + 5


def describe_edge(turns: int, edge_index: int) -> EdgeDescriptor:
    """Classify edge e of truncated polygon Gamma_N."""
    n_outer = 2 * turns + 1
    origin = n_outer
    inner_last = 4 * turns + 2
    inner_start = 2 * turns + 2
    connector_idx = 4 * turns + 3
    degenerate_idx = 4 * turns + 2

    if edge_index < n_outer:
        k = edge_index
        th0 = CANONICAL_THETA0 + k * math.pi / 2.0
        th1 = th0 + math.pi / 2.0
        return EdgeDescriptor(
            edge_index,
            "outer_arm",
            th0,
            th1,
            False,
            f"outer chord gamma_+({th0:.4f}) to gamma_+({th1:.4f})",
        )
    if edge_index == origin:
        return EdgeDescriptor(
            edge_index,
            "origin_to_inner",
            None,
            None,
            True,
            "origin to inner-arm outer sample (truncation seam)",
        )
    if inner_start <= edge_index <= inner_last - 1:
        j = edge_index - inner_start
        k_hi = 2 * turns - j
        k_lo = k_hi - 1
        th0 = CANONICAL_THETA0 + k_lo * math.pi / 2.0
        th1 = CANONICAL_THETA0 + k_hi * math.pi / 2.0
        return EdgeDescriptor(
            edge_index,
            "inner_arm",
            th0,
            th1,
            False,
            f"inner chord gamma_- at half-turns {k_lo},{k_hi}",
        )
    if edge_index == degenerate_idx:
        return EdgeDescriptor(
            edge_index,
            "inner_to_p_minus",
            None,
            None,
            True,
            "inner last vertex to duplicate p_minus (degenerate)",
        )
    if edge_index == connector_idx:
        return EdgeDescriptor(
            edge_index,
            "outer_connector",
            CANONICAL_THETA0,
            CANONICAL_THETA0,
            False,
            "permanent outer connector gamma_-(theta0) to gamma_+(theta0)",
        )
    return EdgeDescriptor(edge_index, "unknown", None, None, True, "unknown")


def hausdorff_to_outer_arm(turns: int) -> float:
    """Sup distance from outer-arm chords to smooth gamma_+ on retained range."""
    canon = CanonicalDoubleSpiral()
    pts = canon.closed_polygon_with_connector(turns)
    n_outer = 2 * turns + 1
    max_d = 0.0
    for i in range(n_outer - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        th0 = CANONICAL_THETA0 + i * math.pi / 2.0
        th1 = th0 + math.pi / 2.0
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            px = (1 - t) * x0 + t * x1
            py = (1 - t) * y0 + t * y1
            th = th0 + t * (th1 - th0)
            sx, sy = gamma_plus(th)
            max_d = max(max_d, math.hypot(px - sx, py - sy))
    return max_d


def macro_square_certificate(turns: int, *, denom: int = 1000) -> MacroSquareCertificate | None:
    poly = rational_truncated_spiral(turns, denom=denom)
    if poly is None:
        return None
    result = solve_polygon_full(poly, allow_repeated_edges=True)
    for cert in result.isolated:
        if cert.edge_indices != MACRO_BRANCH_EDGES:
            continue
        ok = validate_geometry(
            poly,
            cert.edge_indices,
            tuple(Fraction(p) for p in cert.edge_parameters),
        )
        return MacroSquareCertificate(
            turns=turns,
            edge_indices=cert.edge_indices,
            edge_parameters=cert.edge_parameters,
            vertices=cert.vertices,
            side_length_squared=cert.side_length_squared,
            solve_rank=cert.solve_rank,
            validator_ok=ok.ok,
            edge_descriptors=tuple(describe_edge(turns, e) for e in cert.edge_indices),
        )
    return None


def vertex_on_smooth_outer_arm(vertex: tuple[str, str], tol: float = 1e-6) -> bool:
    x = float(Fraction(vertex[0]))
    y = float(Fraction(vertex[1]))
    r = math.hypot(x, y)
    th = math.atan2(y, x)
    return abs(r - r_outer(th)) <= tol


def side_length() -> float:
    return math.sqrt(float(literal_side_length_squared()))


def side_length_lower_bound() -> float:
    """Exact rational side length (macro branch)."""
    return side_length()


def literal_side_length_squared() -> Fraction:
    return Fraction(
        "779802774027925101251181018894122731419976/5520292900471106279627034034189224034018569"
    )


def min_vertex_radius_lower_bound() -> float:
    verts = [
        (Fraction(a), Fraction(b))
        for a, b in [
            ("733231852773421056599/2349530357427012748413", "41530314010052770944/783176785809004249471"),
            ("139975551510597517169/2349530357427012748413", "-529511293893155939942/2349530357427012748413"),
            ("-171375561470905578535/783176785809004249471", "63745007369667599488/2349530357427012748413"),
            ("26376538950035601275/783176785809004249471", "239282414430993950754/783176785809004249471"),
        ]
    ]
    return min(math.hypot(float(x), float(y)) for x, y in verts)


def certificates_identical(a: MacroSquareCertificate, b: MacroSquareCertificate) -> bool:
    return (
        a.edge_indices == b.edge_indices
        and a.edge_parameters == b.edge_parameters
        and a.vertices == b.vertices
        and a.side_length_squared == b.side_length_squared
    )
