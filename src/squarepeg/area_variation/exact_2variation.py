"""Exact squared 2-variation for polygonal paths (vertex-optimal DP)."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Sequence

from squarepeg.area_variation.polygonal_arc import Point

FracPoint = tuple[Fraction, Fraction]


def euclidean_sq(p: Point, q: Point) -> float:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def euclidean_sq_frac(p: FracPoint, q: FracPoint) -> Fraction:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def max_partition_sum_squares(vertices: Sequence[Point]) -> float:
    """
    sup_{partitions} sum |Delta alpha|^2 on polygonal arc with breakpoints at vertices.

    DP: F[j] = max_{0<=i<j} F[i] + |v_j - v_i|^2, F[0]=0.
    For PL paths and p=2, optimal partitions use vertices only (see docs).
    """
    n = len(vertices)
    if n < 2:
        return 0.0
    f = [0.0] * n
    for j in range(1, n):
        best = 0.0
        for i in range(j):
            best = max(best, f[i] + euclidean_sq(vertices[i], vertices[j]))
        f[j] = best
    return f[n - 1]


def squared_2variation(vertices: Sequence[Point]) -> float:
    """|alpha|_{2-var;[s,t]}^2."""
    return max_partition_sum_squares(vertices)


def two_variation_norm(vertices: Sequence[Point]) -> float:
    return math.sqrt(max_partition_sum_squares(vertices))


def max_partition_sum_squares_frac(vertices: Sequence[FracPoint]) -> Fraction:
    n = len(vertices)
    if n < 2:
        return Fraction(0)
    f: list[Fraction] = [Fraction(0)] * n
    for j in range(1, n):
        best = Fraction(0)
        for i in range(j):
            cand = f[i] + euclidean_sq_frac(vertices[i], vertices[j])
            if cand > best:
                best = cand
        f[j] = best
    return f[n - 1]


def diameter(vertices: Sequence[Point]) -> float:
    m = 0.0
    for i, p in enumerate(vertices):
        for q in vertices[i + 1 :]:
            m = max(m, math.sqrt(euclidean_sq(p, q)))
    return m
