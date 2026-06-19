"""Local area defect for area-tightness (T032 program)."""

from __future__ import annotations

import math
from typing import Callable, Sequence

from squarepeg.area_variation.signed_area import relative_area_increment

Point = tuple[float, float]
CurveFn = Callable[[float], Point]


def arc_length_param_distance(gamma: CurveFn, s: float, t: float, n: int = 128) -> float:
    """Proxy for d(s,t): Euclidean distance between gamma(s), gamma(t) on [0,1] params."""
    ps, pt = gamma(s), gamma(t)
    return math.hypot(ps[0] - pt[0], ps[1] - pt[1])


def alpha_P_delta(gamma: CurveFn, delta: float, samples: int = 64) -> float:
    """
    alpha_P(delta) = sup_{d(s,t)<=delta} |A_P(s,t)|.

    Sampled on uniform parameter grid.
    """
    m = 0.0
    step = 1.0 / samples
    params = [i * step for i in range(samples + 1)]
    for i, s in enumerate(params):
        for t in params[i + 1 :]:
            if arc_length_param_distance(gamma, s, t) > delta:
                continue
            # sample arc along parameters
            k = max(2, int(abs(t - s) / step) + 1)
            arc_pts = [gamma(s + (t - s) * j / (k - 1)) for j in range(k)]
            m = max(m, abs(relative_area_increment(arc_pts)))
    return m


def alpha_sequence_limsup(
    gammas: Sequence[CurveFn],
    delta: float,
) -> float:
    """alpha_{(P_n)}(delta) = limsup_n alpha_{P_n}(delta)."""
    if not gammas:
        return 0.0
    vals = [alpha_P_delta(g, delta) for g in gammas]
    return max(vals[-3:]) if len(vals) >= 3 else max(vals)


def is_area_tight_sequence(
    gammas: Sequence[CurveFn],
    deltas: Sequence[float],
    tol: float = 1e-2,
) -> bool:
    """lim_{delta->0} limsup_n alpha_{P_n}(delta) = 0 (sampled test)."""
    for delta in sorted(deltas, reverse=True):
        if alpha_sequence_limsup(gammas, delta) > tol:
            return False
    return True


def polygon_gamma(polygon_vertices: Sequence[Point]) -> CurveFn:
    """PL Jordan parametrization on [0,1]."""
    n = len(polygon_vertices)

    def gamma(t: float) -> Point:
        t = t % 1.0
        f = t * n
        i = int(f) % n
        u = f - int(f)
        p0 = polygon_vertices[i]
        p1 = polygon_vertices[(i + 1) % n]
        return p0[0] + u * (p1[0] - p0[0]), p0[1] + u * (p1[1] - p0[1])

    return gamma
