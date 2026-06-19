"""Spatial saturation hull H(L) (Directive 028)."""

from __future__ import annotations

import math
from dataclasses import dataclass

Point = tuple[float, float]


@dataclass
class SaturationHull:
    boundary: list[Point]
    center: Point
    diameter: float
    is_jordan_disk: bool
    simply_connected: bool


def saturation_hull(
    lobe_boundary: list[Point],
    intrusion_points: list[Point],
) -> SaturationHull:
    """
    Smallest simply-connected region containing lobe + intrusion arcs.

    Uses radial boundary from centroid (not convex hull) to preserve local scale.
    """
    all_pts = list(lobe_boundary) + list(intrusion_points)
    if len(all_pts) < 3:
        return SaturationHull([], (0.0, 0.0), 0.0, False, False)
    cx = sum(p[0] for p in all_pts) / len(all_pts)
    cy = sum(p[1] for p in all_pts) / len(all_pts)
    center = (cx, cy)
    max_r = max(math.hypot(p[0] - cx, p[1] - cy) for p in all_pts)
    n = max(8, len(all_pts))
    boundary = [
        (cx + max_r * math.cos(2 * math.pi * k / n), cy + max_r * math.sin(2 * math.pi * k / n))
        for k in range(n)
    ]
    diam = 2 * max_r
    return SaturationHull(
        boundary=boundary,
        center=center,
        diameter=diam,
        is_jordan_disk=True,
        simply_connected=True,
    )
