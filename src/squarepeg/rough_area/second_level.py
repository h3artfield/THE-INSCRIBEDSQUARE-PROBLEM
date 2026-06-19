"""Second-level area tensors for polygonal paths (exploratory)."""

from __future__ import annotations

import math


def antisymmetric_area_increment(p0, p1) -> float:
    """
    Discrete antisymmetric increment (1/2)[x, dx] ~ (1/2)(x0*dy - y0*dx) on segment.
    Planar: half cross product of position with increment.
    """
    x0, y0 = p0
    dx = p1[0] - x0
    dy = p1[1] - y0
    return 0.5 * (x0 * dy - y0 * dx)


def polygon_area_second_level(points) -> float:
    """Total signed area via shoelace (classical limit of second level for PL)."""
    n = len(points)
    if n < 3:
        return 0.0
    twice = 0.0
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        twice += x0 * y1 - x1 * y0
    return twice / 2.0


def liouville_from_second_level_symmetric(points) -> float:
    """
    For PL path, Liouville integral int xi dx equals signed area term
    when lambda = xi dx (AI convention). Exploratory consistency check.
    """
    acc = 0.0
    for i in range(len(points) - 1):
        x0, xi0 = points[i]
        x1, xi1 = points[i + 1]
        acc += 0.5 * (xi0 + xi1) * (x1 - x0)
    return acc
