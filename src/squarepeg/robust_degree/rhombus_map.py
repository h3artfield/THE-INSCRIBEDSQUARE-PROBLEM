"""Rhombus and diagonal decomposition of the square map."""

from __future__ import annotations

from typing import Callable, Sequence

from squarepeg.robust_degree.square_map import CurveFn, Point

SideSq = tuple[float, float, float, float]


def side_squared(gamma: CurveFn, u: Sequence[float]) -> SideSq:
    pts = [gamma(float(ui)) for ui in u]
    out: list[float] = []
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        out.append((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return (out[0], out[1], out[2], out[3])


def rhombus_map_G(gamma: CurveFn, u: Sequence[float]) -> tuple[float, float, float]:
    """
    G_gamma(u) = (s1-s2, s2-s3, s3-s4) with s_i = |p_i - p_{i+1}|^2.

    G=0 iff all four side lengths agree (rhombus, away from degeneracy).
    """
    s = side_squared(gamma, u)
    return (s[0] - s[1], s[1] - s[2], s[2] - s[3])


def diagonal_defect_D(gamma: CurveFn, u: Sequence[float]) -> float:
    """D_gamma(u) = |p1-p3|^2 - |p2-p4|^2."""
    pts = [gamma(float(ui)) for ui in u]
    d13 = (pts[0][0] - pts[2][0]) ** 2 + (pts[0][1] - pts[2][1]) ** 2
    d24 = (pts[1][0] - pts[3][0]) ** 2 + (pts[1][1] - pts[3][1]) ** 2
    return d13 - d24


def square_map_from_parts(gamma: CurveFn, u: Sequence[float]) -> tuple[float, float, float, float]:
    """F = (G, D) in frozen convention matching square_map_F."""
    g = rhombus_map_G(gamma, u)
    d = diagonal_defect_D(gamma, u)
    return (g[0], g[1], g[2], d)


def is_square_configuration(
    gamma: CurveFn,
    u: Sequence[float],
    *,
    side_tol: float = 1e-8,
    diagonal_tol: float = 1e-8,
    min_side: float = 1e-10,
) -> bool:
    """G=0 and D=0 with positive side length => nondegenerate square."""
    g = rhombus_map_G(gamma, u)
    if max(abs(x) for x in g) > side_tol:
        return False
    if abs(diagonal_defect_D(gamma, u)) > diagonal_tol:
        return False
    s = side_squared(gamma, u)
    side = min(s) ** 0.5
    return side >= min_side


def rhombus_implies_equal_sides(gamma: CurveFn, u: Sequence[float], tol: float = 1e-12) -> bool:
    g = rhombus_map_G(gamma, u)
    return max(abs(x) for x in g) <= tol
