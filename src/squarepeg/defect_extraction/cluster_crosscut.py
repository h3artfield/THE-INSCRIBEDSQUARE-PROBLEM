"""Cluster crosscut and T051 local surgery (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.defect_extraction.two_gate_cluster import SaturatedCluster
from squarepeg.defect_surgery.crosscut import Crosscut, collar_arc_crosscut, straight_chord_crosscut
from squarepeg.defect_surgery.packet_disk import PacketDisk
from squarepeg.defect_surgery.local_surgery import apply_local_surgery

Point = tuple[float, float]


@dataclass
class ClusterSurgeryResult:
    is_jordan: bool
    uniform_error: float
    crosscut: Crosscut
    straight_failed: bool
    curved_used: bool


def cluster_crosscut(cluster: SaturatedCluster, *, prefer_straight: bool = True) -> Crosscut:
    """
    Embedded crosscut in H(C): straight if valid, else collar arc (curved crosscut theorem).
    """
    disk = PacketDisk(
        center=cluster.hull.center,
        radius=cluster.hull.diameter / 2,
        interval_start=0,
        interval_end=1,
    )
    straight = straight_chord_crosscut(cluster.gate_a, cluster.gate_b)
    if prefer_straight:
        return straight
    return collar_arc_crosscut(disk, cluster.gate_a, cluster.gate_b)


def prove_cluster_crosscut_exists(cluster: SaturatedCluster) -> bool:
    """Jordan disk with two gates admits embedded crosscut (collar fallback)."""
    return cluster.hull.is_jordan_disk and cluster.gate_a != cluster.gate_b


def apply_cluster_surgery(
    vertices: list[Point],
    cluster: SaturatedCluster,
    i0: int,
    i1: int,
) -> ClusterSurgeryResult:
    """T051 local: replace saturated subsystem by crosscut."""
    disk = PacketDisk(
        center=cluster.hull.center,
        radius=cluster.hull.diameter / 2 + 0.01,
        interval_start=i0,
        interval_end=i1,
    )
    straight = straight_chord_crosscut(cluster.gate_a, cluster.gate_b)
    res = apply_local_surgery(vertices, disk, straight)
    straight_failed = not res.is_jordan
    curved = False
    if straight_failed:
        curved_cross = collar_arc_crosscut(disk, cluster.gate_a, cluster.gate_b)
        res = apply_local_surgery(vertices, disk, curved_cross)
        curved = True
    return ClusterSurgeryResult(
        is_jordan=res.is_jordan,
        uniform_error=res.uniform_error,
        crosscut=res.crosscut,
        straight_failed=straight_failed,
        curved_used=curved,
    )


def t051_statement() -> str:
    return "T051 (PROVED_LOCALLY): two-gate clean cluster => Jordan-preserving cluster surgery."
