"""Yang partition area operators (YANG-AREA-v1 notation)."""

from __future__ import annotations

import math
from typing import Callable, Sequence

Point = tuple[float, float]
CurveFn = Callable[[float], Point]


def partition_mesh(partition: Sequence[float]) -> float:
    """Yang Notation 2: |D| = max |t_{j+1} - t_j|."""
    if len(partition) < 2:
        return 0.0
    return max(partition[i + 1] - partition[i] for i in range(len(partition) - 1))


def yang_pl_interpolant(curve: CurveFn, partition: Sequence[float], t: float) -> Point:
    """
    Yang Notation 9, eq. (4): piecewise-linear path gamma^D agreeing with gamma on D.

    On [t_j, t_{j+1}]:
        gamma^D(t) = ((t - t_j)/(t_{j+1} - t_j)) gamma(t_{j+1})
                   + ((t_{j+1} - t)/(t_{j+1} - t_j)) gamma(t_j).
    """
    if t <= partition[0]:
        return curve(partition[0])
    if t >= partition[-1]:
        return curve(partition[-1])
    for j in range(len(partition) - 1):
        t0, t1 = partition[j], partition[j + 1]
        if t0 <= t <= t1:
            if t1 == t0:
                return curve(t0)
            w = (t - t0) / (t1 - t0)
            p0, p1 = curve(t0), curve(t1)
            return (p0[0] + w * (p1[0] - p0[0]), p0[1] + w * (p1[1] - p0[1]))
    return curve(partition[-1])


def sample_yang_pl(curve: CurveFn, partition: Sequence[float]) -> list[Point]:
    """Evaluate gamma^D at partition nodes (equals gamma at nodes)."""
    return [curve(t) for t in partition]


def lie_bracket_scalar(p0: Point, p1: Point) -> float:
    """Scalar coefficient of [v1, v2] in R^2 with basis [e_x, e_xi]: x1*xi2 - xi1*x2."""
    x0, xi0 = p0
    x1, xi1 = p1
    return x0 * xi1 - xi0 * x1


def yang_area_increment(points: Sequence[Point], i: int, j: int) -> float:
    """
    A(gamma^D)(t_i, t_j) scalar on [V,V] for planar embedding.

    Yang page 10: A(gamma^D)(s,t) = 1/2 sum_{k in D cap [s,t]} [gamma(tk), gamma(tk+1)]
                                   - 1/2 [gamma(s), gamma(t)].
    """
    if j <= i:
        return 0.0
    acc = 0.0
    for k in range(i, j):
        acc += lie_bracket_scalar(points[k], points[k + 1])
    return 0.5 * acc - 0.5 * lie_bracket_scalar(points[i], points[j])


def yang_area_on_partition(points: Sequence[Point]) -> list[float]:
    """a(0, t_i) for each partition index."""
    return [yang_area_increment(points, 0, i) for i in range(len(points))]


def area_1variation_seminorm_on_grid(area_values: Sequence[float]) -> float:
    """1-variation seminorm of area function t -> a(0,t) on partition grid."""
    if len(area_values) < 2:
        return 0.0
    return sum(abs(area_values[i + 1] - area_values[i]) for i in range(len(area_values) - 1))


def area_difference_1var(points_a: Sequence[Point], points_b: Sequence[Point]) -> float:
    """
    ||A(gamma^{D1}) - A(gamma^{D2})||_{1-var} on common refined grid (exploratory).

    When partitions differ, compare a(0,.) on the union partition samples.
    """
    if len(points_a) != len(points_b):
        raise ValueError("common partition required")
    aa = yang_area_on_partition(points_a)
    ab = yang_area_on_partition(points_b)
    return sum(abs(x - y) for x, y in zip(aa, ab))


def theorem33_cauchy_bound(
    m_delta: float,
    c_modulus: float,
    integral_m_sq_over_r: float,
) -> float:
    """
    Yang Thm 33 proof (page 38), p=q=2, m1=m2=m:

    ||A(gamma^{D1}) - A(gamma^{D2})||_{1-var}
        <= 2 C^2 ( 2 m(delta) + m(delta)^2 + 2 int_0^delta m(t)^2/t dt )
    """
    return 2.0 * c_modulus * c_modulus * (
        2.0 * m_delta + m_delta * m_delta + 2.0 * integral_m_sq_over_r
    )


def m_sq_integral_approx(m_fn: Callable[[float], float], delta: float, steps: int = 500) -> float:
    """Numerical int_0^delta m(t)^2/t dt."""
    if delta <= 0:
        return 0.0
    total = 0.0
    for i in range(1, steps + 1):
        t = delta * i / steps
        prev = delta * (i - 1) / steps
        m = m_fn(t)
        total += (m * m / max(t, 1e-15)) * (t - prev)
    return total


def partitions_cauchy_on_circle(
    curve: CurveFn,
    meshes: Sequence[float],
) -> list[float]:
    """Area 1-var differences between dyadic uniform partitions (exploratory)."""
    diffs: list[float] = []
    prev: list[Point] | None = None
    for h in meshes:
        n = max(2, int(math.ceil(1.0 / h)))
        part = [i / n for i in range(n + 1)]
        pts = sample_yang_pl(curve, part)
        if prev is not None:
            diffs.append(area_difference_1var(prev, pts))
        prev = pts
    return diffs
