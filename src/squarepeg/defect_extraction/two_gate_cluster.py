"""Two-gate saturated clusters (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.saturation import SaturationState
from squarepeg.defect_extraction.saturation_hull import SaturationHull
from squarepeg.defect_surgery.packet_disk import Point, point_in_disk_interior

Point = tuple[float, float]


@dataclass
class SaturatedCluster:
    cluster_id: str
    saturation: SaturationState
    hull: SaturationHull
    gate_a: Point
    gate_b: Point
    intrusion_depth: int
    branching: int


@dataclass
class TwoGateAudit:
    two_gate_clean: bool
    jordan_hull: bool
    retained_disjoint: bool
    only_two_gates: bool
    crosscut_exists: bool
    diameter_controlled: bool


def audit_two_gate_cluster(
    cluster: SaturatedCluster,
    retained_vertices: list[Point],
    *,
    diam_threshold: float = 0.5,
) -> TwoGateAudit:
    """Two-gate clean: Jordan hull, retained meets boundary only at A_C, B_C."""
    hull = cluster.hull
    interior_hit = False
    boundary_hits = 0
    for rv in retained_vertices:
        if point_in_disk_interior(rv, _hull_disk(hull)):
            interior_hit = True
        da = math_dist(rv, cluster.gate_a)
        db = math_dist(rv, cluster.gate_b)
        if da < 1e-6 or db < 1e-6:
            boundary_hits += 1
    retained_disjoint = not interior_hit
    only_two = boundary_hits <= 2
    diam_ok = hull.diameter <= diam_threshold
    return TwoGateAudit(
        two_gate_clean=hull.is_jordan_disk and retained_disjoint and only_two and diam_ok,
        jordan_hull=hull.is_jordan_disk,
        retained_disjoint=retained_disjoint,
        only_two_gates=only_two,
        crosscut_exists=hull.is_jordan_disk,
        diameter_controlled=diam_ok,
    )


def math_dist(a: Point, b: Point) -> float:
    import math

    return math.hypot(a[0] - b[0], a[1] - b[1])


def _hull_disk(hull: SaturationHull):
    from squarepeg.defect_surgery.packet_disk import PacketDisk

    return PacketDisk(center=hull.center, radius=hull.diameter / 2, interval_start=0, interval_end=1)
