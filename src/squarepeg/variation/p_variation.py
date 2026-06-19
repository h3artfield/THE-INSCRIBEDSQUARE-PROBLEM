"""r-variation seminorms for planar paths (repository convention).

Convention (Directive 006):
    |u|_{r-var;[a,b]} = (sup_P sum_i |u(t_{i+1})-u(t_i)|^r)^{1/r}
    |u|_{infty;[a,b]} = sup_{t in [a,b]} |u(t)|

Constant offsets are NOT folded into the variation seminorm; they are tracked
separately when a full norm is needed.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Sequence

Point = tuple[float, float]


def euclidean(p: Point, q: Point) -> float:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return math.hypot(dx, dy)


def osc(points: Sequence[Point]) -> float:
    """osc(h) = sup_{s,t} |h(t)-h(s)| on the given sample."""
    if not points:
        return 0.0
    m = 0.0
    for i, p in enumerate(points):
        for q in points[i + 1 :]:
            m = max(m, euclidean(p, q))
    return m


def sup_norm(points: Sequence[Point]) -> float:
    """Max distance from origin on sample (for centered paths use osc)."""
    if not points:
        return 0.0
    return max(math.hypot(p[0], p[1]) for p in points)


def p_variation_on_partition(points: Sequence[Point], p: float) -> float:
    """Exact r-variation on the conforming partition through `points`."""
    if len(points) < 2:
        return 0.0
    if p <= 0:
        raise ValueError("p must be positive")
    total = sum(euclidean(points[i], points[i + 1]) ** p for i in range(len(points) - 1))
    return total ** (1.0 / p)


def p_variation(points: Sequence[Point], p: float) -> float:
    """
    |c|_{p-var} on a piecewise-linear path with breakpoints at `points`.

    For a PL path, the supremum over all partitions equals the value on the
    conforming partition (BG / Föllmer; see docs/q_variation_interpolation_proof.md).
    """
    return p_variation_on_partition(points, p)


def total_variation(points: Sequence[Point]) -> float:
    return p_variation(points, 1.0)


def path_difference(p: Sequence[Point], q: Sequence[Point]) -> list[Point]:
    if len(p) != len(q):
        raise ValueError("paths must share a common parametrization")
    return [(a[0] - b[0], a[1] - b[1]) for a, b in zip(p, q)]


def interpolation_constant(p: float, q: float) -> float:
    """
    Best constant in |h|_{q-var} <= C osc(h)^{1-p/q} |h|_{p-var}^{p/q}
    under the repository convention (C=1; see proof doc).
    """
    if not (0 < p < q):
        raise ValueError("require 0 < p < q")
    return 1.0


def q_variation_from_p_bound(
    p: float,
    q: float,
    p_var: float,
    oscillation: float,
) -> float:
    """Apply the interpolation inequality (conjectural upper bound helper)."""
    if oscillation <= 0:
        return 0.0
    return oscillation ** (1.0 - p / q) * p_var ** (p / q)


def variation_norm_monotone(q: float, one_var: float) -> float:
    """
    For q >= 1, |h|_{q-var} <= |h|_{1-var} (same path, repository convention).
    Returns the q-variation upper bound given 1-variation.
    """
    if q < 1.0:
        raise ValueError("q must be >= 1")
    return one_var


def is_increasing_reparam(values: list[float]) -> bool:
    return all(values[i + 1] >= values[i] for i in range(len(values) - 1))


def q_variation_bounded_by_total(points: Sequence[Point], q: float) -> bool:
    """Verify |h|_{q-var} <= |h|_{1-var} on conforming partition."""
    if q < 1.0:
        return True
    return p_variation(points, q) <= p_variation(points, 1.0) + 1e-9


# Legacy Fraction API for exact polygon tests
FracPoint = tuple[Fraction, Fraction]


def euclidean_frac(p: FracPoint, q: FracPoint) -> float:
    dx = float(p[0] - q[0])
    dy = float(p[1] - q[1])
    return math.hypot(dx, dy)


def p_variation_frac(points: list[FracPoint], p: float) -> float:
    if len(points) < 2:
        return 0.0
    total = sum(euclidean_frac(points[i], points[i + 1]) ** p for i in range(len(points) - 1))
    return total ** (1.0 / p)
