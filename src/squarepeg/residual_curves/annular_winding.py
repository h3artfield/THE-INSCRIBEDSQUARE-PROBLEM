"""Annular winding certificates for spiral obstruction."""

from __future__ import annotations

import math
from dataclasses import dataclass

Point = tuple[float, float]


@dataclass(frozen=True)
class Annulus:
    inner: float
    outer: float


def winding_about_point(polyline: list[Point], center: Point) -> int:
    """Discrete winding number of closed polyline about center (exploratory)."""
    cx, cy = center
    total = 0.0
    n = len(polyline)
    if n < 3:
        return 0
    for i in range(n):
        x0, y0 = polyline[i]
        x1, y1 = polyline[(i + 1) % n]
        a0 = math.atan2(y0 - cy, x0 - cx)
        a1 = math.atan2(y1 - cy, x1 - cx)
        da = a1 - a0
        if da > math.pi:
            da -= 2 * math.pi
        if da < -math.pi:
            da += 2 * math.pi
        total += da
    return int(round(total / (2 * math.pi)))


def area_lower_bound_from_winding(wind: int, annulus: Annulus) -> float:
    """Crude lower bound: |wind| * pi * (r_out^2 - r_in^2) / 2 if wind full turn."""
    if wind == 0:
        return 0.0
    return abs(wind) * math.pi * (annulus.outer**2 - annulus.inner**2) / 2.0
