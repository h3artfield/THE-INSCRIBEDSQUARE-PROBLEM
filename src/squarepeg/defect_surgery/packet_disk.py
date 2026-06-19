"""Isolated packet disk validation (Directive 023)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

Point = tuple[float, float]


@dataclass(frozen=True)
class PacketDisk:
    """Closed Jordan disk D with diameter r containing packet interval image."""

    center: Point
    radius: float
    interval_start: int
    interval_end: int  # inclusive vertex indices on polygon

    @property
    def diameter(self) -> float:
        return 2.0 * self.radius


def dist(p: Point, q: Point) -> float:
    return math.hypot(p[0] - q[0], p[1] - q[1])


def point_in_disk(p: Point, disk: PacketDisk, tol: float = 1e-9) -> bool:
    return dist(p, disk.center) <= disk.radius + tol


def point_in_disk_interior(p: Point, disk: PacketDisk, tol: float = 1e-9) -> bool:
    return dist(p, disk.center) < disk.radius - tol


@dataclass
class IsolationAudit:
    is_isolated: bool
    diameter_ok: bool
    endpoints_on_boundary: bool
    interior_in_int: bool
    exterior_disjoint: bool
    checks: dict[str, bool] = field(default_factory=dict)


def validate_isolated_packet(
    vertices: list[Point],
    disk: PacketDisk,
    *,
    max_diameter: float | None = None,
) -> IsolationAudit:
    """
    Verify isolated packet disk conditions (Directive 023 §3).
    """
    n = len(vertices)
    if n < 3:
        return IsolationAudit(False, False, False, False, False)

    i0, i1 = disk.interval_start, disk.interval_end
    if i0 > i1:
        i0, i1 = i1, i0
    interval_indices = list(range(i0, i1 + 1))

    diameter_ok = disk.diameter <= (max_diameter if max_diameter is not None else disk.diameter + 1)
    if max_diameter is not None:
        diameter_ok = disk.diameter <= max_diameter

    p_a = vertices[i0]
    p_b = vertices[i1]
    endpoints_on_boundary = (
        abs(dist(p_a, disk.center) - disk.radius) < 1e-6
        and abs(dist(p_b, disk.center) - disk.radius) < 1e-6
    )

    interior_in_int = all(
        point_in_disk_interior(vertices[i], disk) or i in (i0, i1) for i in interval_indices[1:-1]
    ) if len(interval_indices) > 2 else True

    exterior_disjoint = True
    for j in range(n):
        if j in interval_indices:
            continue
        if point_in_disk_interior(vertices[j], disk):
            exterior_disjoint = False
            break

    checks = {
        "diameter": diameter_ok,
        "endpoints_boundary": endpoints_on_boundary,
        "interior_in_int": interior_in_int,
        "exterior_disjoint": exterior_disjoint,
    }
    return IsolationAudit(
        is_isolated=all(checks.values()),
        diameter_ok=diameter_ok,
        endpoints_on_boundary=endpoints_on_boundary,
        interior_in_int=interior_in_int,
        exterior_disjoint=exterior_disjoint,
        checks=checks,
    )


def disk_from_interval(vertices: list[Point], i0: int, i1: int, padding: float = 0.05) -> PacketDisk:
    """Construct minimal bounding disk for interval vertices."""
    idxs = list(range(min(i0, i1), max(i0, i1) + 1))
    pts = [vertices[i] for i in idxs]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    r = max(dist(p, (cx, cy)) for p in pts) + padding
    return PacketDisk(center=(cx, cy), radius=r, interval_start=min(i0, i1), interval_end=max(i0, i1))
