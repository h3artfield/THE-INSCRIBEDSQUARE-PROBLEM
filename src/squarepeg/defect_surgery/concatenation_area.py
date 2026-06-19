"""Chen concatenation identity for relative area (Directive 024)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.area_variation.signed_area import lie_bracket_scalar, relative_area_increment

Point = tuple[float, float]


def wedge(a: Point, b: Point) -> float:
    """(a_1,a_2) wedge (b_1,b_2) = a_1 b_2 - a_2 b_1."""
    return a[0] * b[1] - a[1] * b[0]


def relative_area_path(points: list[Point]) -> float:
    """A_X(s,t) for polygonal path with fixed start at points[0]."""
    return relative_area_increment(points)


def chen_identity_three(
    x_s: Point,
    x_u: Point,
    x_t: Point,
    path_su: list[Point],
    path_ut: list[Point],
    path_st: list[Point],
    *,
    tol: float = 1e-9,
) -> bool:
    """
    Verify A(s,t) = A(s,u) + A(u,t) + 1/2 (X(u)-X(s)) wedge (X(t)-X(u)).
    """
    a_su = relative_area_path(path_su)
    a_ut = relative_area_path(path_ut)
    a_st = relative_area_path(path_st)
    inc = 0.5 * wedge((x_u[0] - x_s[0], x_u[1] - x_s[1]), (x_t[0] - x_u[0], x_t[1] - x_u[1]))
    return abs(a_st - (a_su + a_ut + inc)) <= tol


@dataclass
class ConcatenationDecomposition:
    component_areas: list[float]
    wedge_terms: list[float]
    total: float
    reconstructed: float


def concatenate_paths(*paths: list[Point]) -> list[Point]:
    """Concatenate polygonal paths (drop duplicate junctions)."""
    if not paths:
        return []
    out = list(paths[0])
    for p in paths[1:]:
        if p and out and p[0] == out[-1]:
            out.extend(p[1:])
        else:
            out.extend(p)
    return out


def finite_concatenation_identity(paths: list[list[Point]]) -> ConcatenationDecomposition:
    """
    For X = X^(1) * ... * X^(m), compute sum of component areas + pairwise wedge terms.
    """
    if not paths:
        return ConcatenationDecomposition([], [], 0.0, 0.0)
    comp = [relative_area_path(p) for p in paths]
    wedges: list[float] = []
    for i in range(len(paths) - 1):
        start_i = paths[i][0]
        end_i = paths[i][-1]
        start_next = paths[i + 1][0]
        end_next = paths[i + 1][-1]
        # Shared junction: end_i == start_next; Chen increment uses (u-s) wedge (t-u)
        wedges.append(
            0.5
            * wedge(
                (end_i[0] - start_i[0], end_i[1] - start_i[1]),
                (end_next[0] - end_i[0], end_next[1] - end_i[1]),
            )
        )
    full = concatenate_paths(*paths)
    total = sum(comp) + sum(wedges)
    recon = relative_area_path(full)
    return ConcatenationDecomposition(
        component_areas=comp,
        wedge_terms=wedges,
        total=total,
        reconstructed=recon,
    )


def chen_identity_holds(paths: list[list[Point]], tol: float = 1e-8) -> bool:
    dec = finite_concatenation_identity(paths)
    return abs(dec.total - dec.reconstructed) <= tol
