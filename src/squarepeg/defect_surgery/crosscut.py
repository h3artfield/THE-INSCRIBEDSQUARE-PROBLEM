"""Replacement crosscuts for packet surgery (Directive 023)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.packet_disk import Point, PacketDisk, dist

CrosscutKind = Literal["straight_chord", "collar_arc"]


@dataclass
class Crosscut:
    """Simple arc from P(a) to P(b) replacing packet interior."""

    start: Point
    end: Point
    interior_points: list[Point]
    kind: CrosscutKind

    def all_points(self) -> list[Point]:
        return [self.start, *self.interior_points, self.end]


def straight_chord_crosscut(start: Point, end: Point) -> Crosscut:
    return Crosscut(start=start, end=end, interior_points=[], kind="straight_chord")


def collar_arc_crosscut(
    disk: PacketDisk,
    start: Point,
    end: Point,
    n_samples: int = 8,
) -> Crosscut:
    """Circular arc in collar between start and end inside disk."""
    cx, cy = disk.center
    r = disk.radius * 0.85
    a0 = math.atan2(start[1] - cy, start[0] - cx)
    a1 = math.atan2(end[1] - cy, end[0] - cx)
    if a1 < a0:
        a1 += 2 * math.pi
    pts: list[Point] = []
    for k in range(1, n_samples):
        t = k / n_samples
        ang = a0 + t * (a1 - a0)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return Crosscut(start=start, end=end, interior_points=pts, kind="collar_arc")


def crosscut_in_disk(cross: Crosscut, disk: PacketDisk, tol: float = 1e-6) -> bool:
    """Interior lies in int(D); endpoints on boundary."""
    from squarepeg.defect_surgery.packet_disk import point_in_disk_interior

    for p in cross.interior_points:
        if not point_in_disk_interior(p, disk, tol=-tol):
            if dist(p, disk.center) >= disk.radius - tol:
                return False
    return True


def chord_intersects_retained(
    cross: Crosscut,
    retained_vertices: list[Point],
    *,
    exclude_endpoints: bool = True,
) -> bool:
    """Check if crosscut segments intersect retained polygon edges (excluding endpoints)."""
    cross_pts = cross.all_points()
    n_ret = len(retained_vertices)
    for i in range(len(cross_pts) - 1):
        c0, c1 = cross_pts[i], cross_pts[i + 1]
        for j in range(n_ret):
            r0 = retained_vertices[j]
            r1 = retained_vertices[(j + 1) % n_ret]
            if _segments_proper_intersect(c0, c1, r0, r1):
                return True
    return False


def _segments_proper_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    return (
        ((d1 > 1e-12 and d2 < -1e-12) or (d1 < -1e-12 and d2 > 1e-12))
        and ((d3 > 1e-12 and d4 < -1e-12) or (d3 < -1e-12 and d4 > 1e-12))
    )
