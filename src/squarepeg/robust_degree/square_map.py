"""Abstract square map on ordered four-window configurations."""

from __future__ import annotations

import math
from typing import Callable, Sequence

Point = tuple[float, float]
CurveFn = Callable[[float], Point]
WindowBox = tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]


def square_map_F(
    gamma: CurveFn,
    u: Sequence[float],
    *,
    windows: WindowBox | None = None,
) -> list[float]:
    """
    F_gamma(u) with u_i interpreted as normalized parameter in J_i = [lo_i, hi_i].

    If windows is None, each u_i is used directly as circle parameter.
    """
    if windows is None:
        thetas = list(u)
    else:
        thetas = [lo + ui * (hi - lo) for ui, (lo, hi) in zip(u, windows)]
    pts = [gamma(t) for t in thetas]

    def sq(a: Point, b: Point) -> float:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    return [
        sq(pts[0], pts[1]) - sq(pts[1], pts[2]),
        sq(pts[1], pts[2]) - sq(pts[2], pts[3]),
        sq(pts[2], pts[3]) - sq(pts[3], pts[0]),
        sq(pts[0], pts[2]) - sq(pts[1], pts[3]),
    ]


def jacobian_F(
    gamma: CurveFn,
    u: Sequence[float],
    *,
    windows: WindowBox | None = None,
    eps: float = 1e-7,
) -> list[list[float]]:
    f0 = square_map_F(gamma, u, windows=windows)
    n = 4
    jac = [[0.0] * n for _ in range(n)]
    for j in range(n):
        up = list(u)
        up[j] += eps
        fj = square_map_F(gamma, up, windows=windows)
        for i in range(n):
            jac[i][j] = (fj[i] - f0[i]) / eps
    return jac


def det4(m: list[list[float]]) -> float:
    a = m
    return (
        a[0][0] * (a[1][1] * (a[2][2] * a[3][3] - a[2][3] * a[3][2])
                   - a[1][2] * (a[2][1] * a[3][3] - a[2][3] * a[3][1])
                   + a[1][3] * (a[2][1] * a[3][2] - a[2][2] * a[3][1]))
        - a[0][1] * (a[1][0] * (a[2][2] * a[3][3] - a[2][3] * a[3][2])
                     - a[1][2] * (a[2][0] * a[3][3] - a[2][3] * a[3][0])
                     + a[1][3] * (a[2][0] * a[3][2] - a[2][2] * a[3][0]))
        + a[0][2] * (a[1][0] * (a[2][1] * a[3][3] - a[2][3] * a[3][1])
                     - a[1][1] * (a[2][0] * a[3][3] - a[2][3] * a[3][0])
                     + a[1][3] * (a[2][0] * a[3][1] - a[2][1] * a[3][0]))
        - a[0][3] * (a[1][0] * (a[2][1] * a[3][2] - a[2][2] * a[3][1])
                     - a[1][1] * (a[2][0] * a[3][2] - a[2][2] * a[3][0])
                     + a[1][2] * (a[2][0] * a[3][1] - a[2][1] * a[3][0]))
    )


def side_length_at(gamma: CurveFn, u: Sequence[float], *, windows: WindowBox | None = None) -> float:
    if windows is None:
        p0, p1 = gamma(u[0]), gamma(u[1])
    else:
        t0 = windows[0][0] + u[0] * (windows[0][1] - windows[0][0])
        t1 = windows[1][0] + u[1] * (windows[1][1] - windows[1][0])
        p0, p1 = gamma(t0), gamma(t1)
    return math.hypot(p0[0] - p1[0], p0[1] - p1[1])


def vertices_at(
    gamma: CurveFn,
    u: Sequence[float],
    *,
    windows: WindowBox | None = None,
) -> list[Point]:
    if windows is None:
        return [gamma(ui) for ui in u]
    return [
        gamma(lo + ui * (hi - lo))
        for ui, (lo, hi) in zip(u, windows)
    ]


def curve_diameter(gamma: CurveFn, samples: int = 256) -> float:
    pts = [gamma(i / samples) for i in range(samples)]
    m = 0.0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            m = max(m, math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]))
    return m


def curve_sup_norm(gamma: CurveFn, samples: int = 256) -> float:
    return max(math.hypot(p[0], p[1]) for p in (gamma(i / samples) for i in range(samples)))
