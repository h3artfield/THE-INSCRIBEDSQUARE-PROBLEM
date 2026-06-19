"""Liouville primitive recovery from Yang antisymmetric area (Directive 008R)."""

from __future__ import annotations

from typing import Sequence

from squarepeg.rough_area.yang_partition_area import lie_bracket_scalar, yang_area_increment
from squarepeg.variation.young_integral import primitive_from_points

Point = tuple[float, float]


def antisymmetric_area_scalar(points: Sequence[Point], i: int, j: int) -> float:
    """Scalar a_c(t_i, t_j) matching Yang A(gamma^D) on R^2."""
    return yang_area_increment(points, i, j)


def trapezoid_xi_dx(points: Sequence[Point], i: int, j: int) -> float:
    """Trapezoidal int_{t_i}^{t_j} xi dx along PL path."""
    acc = 0.0
    for k in range(i, j):
        x0, xi0 = points[k]
        x1, xi1 = points[k + 1]
        acc += 0.5 * (xi0 + xi1) * (x1 - x0)
    return acc


def liouville_integral(points: Sequence[Point], i: int, j: int) -> float:
    """
    int_{t_i}^{t_j} xi dx = (xi(s)+xi(t))/2 (x(t)-x(s)) - a_c(s,t).

    AI-PEG-v3: c=(x, xi), lambda=xi dx.
    """
    x0, xi0 = points[i]
    x1, xi1 = points[j]
    endpoint = 0.5 * (xi0 + xi1) * (x1 - x0)
    return endpoint - antisymmetric_area_scalar(points, i, j)


def recover_primitive(points: Sequence[Point]) -> list[float]:
    """f(t_i) with f(0)=0 via area recovery."""
    n = len(points)
    return [liouville_integral(points, 0, i) for i in range(n)]


def liouville_matches_trapezoid(points: Sequence[Point], tol: float = 1e-10) -> bool:
    """On straight-segment PL, trapezoid and area formula agree."""
    prim_area = recover_primitive(points)
    prim_trap = primitive_from_points(list(points))
    return all(abs(a - b) < tol for a, b in zip(prim_area, prim_trap))


def closed_period_integral(points: Sequence[Point]) -> float:
    prims = recover_primitive(points)
    return prims[-1] - prims[0] if prims else 0.0


def bracket_segment(p0: Point, p1: Point) -> float:
    """1/2 [p0, p1] scalar."""
    return 0.5 * lie_bracket_scalar(p0, p1)
