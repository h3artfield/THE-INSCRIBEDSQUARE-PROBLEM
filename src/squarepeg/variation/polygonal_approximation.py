"""Piecewise-linear Jordan approximants (BG-INTERPOLATION-v2 interface).

In R^2, minimizing geodesics are straight segments; BG Theorem 2.2 yields
simple chord polygons with mesh -> 0. Lemma 3.1 (identity f) gives q-variation
convergence for q > p.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.variation.p_variation import Point, p_variation


def mesh_size(points: list[Point]) -> float:
    if len(points) < 2:
        return 0.0
    from squarepeg.variation.p_variation import euclidean

    return max(euclidean(points[i], points[i + 1]) for i in range(len(points) - 1))


def chord_polygon(points: list[Point]) -> list[Point]:
    """Connect samples in cyclic parameter order (PL interpolation)."""
    return list(points)


def sample_uniform(curve_fn, n: int) -> list[Point]:
    """Uniform parameter samples t_i = i/n on [0,1]."""
    return [curve_fn(i / n) for i in range(n)] + [curve_fn(1.0)]


def sample_refined(curve_fn, n: int) -> list[Point]:
    """Refined partition including midpoints (exploratory mesh control)."""
    pts: list[Point] = []
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        pts.append(curve_fn(t0))
        pts.append(curve_fn(0.5 * (t0 + t1)))
    pts.append(curve_fn(1.0))
    return pts


def polygon_p_variation(points: list[Point], p: float) -> float:
    return p_variation(points, p)


def difference_paths(a: list[Point], b: list[Point]) -> list[Point]:
    if len(a) != len(b):
        raise ValueError("common parametrization required")
    return [(x[0] - y[0], x[1] - y[1]) for x, y in zip(a, b)]


@dataclass(frozen=True)
class PolygonalApproximation:
    """PL interpolant P_n = c^{Pi_n} on a shared partition."""

    partition_times: list[float]
    original: list[Point]
    interpolant: list[Point]

    @property
    def mesh(self) -> float:
        return mesh_size(self.interpolant)


def piecewise_linear_interpolation(
    curve_fn,
    partition: list[float],
) -> PolygonalApproximation:
    """
    Build gamma^{P} at partition points (BG specialization M=R^2).

    `curve_fn` must be a Jordan parametrization on [0,1].
    """
    if partition[0] != 0.0 or partition[-1] != 1.0:
        raise ValueError("partition must start at 0 and end at 1")
    original = [curve_fn(t) for t in partition]
    return PolygonalApproximation(
        partition_times=list(partition),
        original=original,
        interpolant=chord_polygon(original),
    )


def dyadic_partitions(max_level: int) -> list[list[float]]:
    """Partitions 0, 1/2^k, 2/2^k, ... for mesh -> 0."""
    out: list[list[float]] = []
    for k in range(1, max_level + 1):
        step = 1.0 / (2**k)
        out.append([i * step for i in range(2**k + 1)])
    return out


def circle_param(t: float, radius: float = 1.0) -> Point:
    return (radius * math.cos(2 * math.pi * t), radius * math.sin(2 * math.pi * t))


def ellipse_param(t: float, a: float = 2.0, b: float = 1.0) -> Point:
    return (a * math.cos(2 * math.pi * t), b * math.sin(2 * math.pi * t))
