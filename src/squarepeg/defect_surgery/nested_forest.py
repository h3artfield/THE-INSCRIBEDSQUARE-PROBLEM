"""Nested and disjoint packet forest surgery (Directive 023)."""

from __future__ import annotations

from dataclasses import dataclass, field

from squarepeg.defect_surgery.local_surgery import SurgeryResult, apply_local_surgery
from squarepeg.defect_surgery.packet_disk import PacketDisk, Point


@dataclass
class PacketForest:
    disks: list[PacketDisk]
    parent: dict[int, int | None] = field(default_factory=dict)


def disks_disjoint(d1: PacketDisk, d2: PacketDisk) -> bool:
    from squarepeg.defect_surgery.packet_disk import dist

    return dist(d1.center, d2.center) >= d1.radius + d2.radius


def forest_is_admissible(forest: PacketForest) -> bool:
    """Disjoint or nested (one contains other's center with larger radius)."""
    ds = forest.disks
    for i in range(len(ds)):
        for j in range(i + 1, len(ds)):
            a, b = ds[i], ds[j]
            if disks_disjoint(a, b):
                continue
            if a.radius >= b.radius and a.center == b.center:
                continue
            if b.radius >= a.radius and b.center == a.center:
                continue
            return False
    return True


def maximal_disks(forest: PacketForest) -> list[PacketDisk]:
    """Replace only maximal selected disks (removes descendant tree)."""
    ds = forest.disks
    maximal: list[PacketDisk] = []
    for i, d in enumerate(ds):
        is_child = False
        for j, e in enumerate(ds):
            if i == j:
                continue
            if e.radius > d.radius and not disks_disjoint(e, d):
                is_child = True
                break
        if not is_child:
            maximal.append(d)
    return maximal


def surgery_order(forest: PacketForest) -> list[PacketDisk]:
    """Outside-in: largest disks first for nested; arbitrary for disjoint."""
    return sorted(forest.disks, key=lambda d: -d.radius)


def apply_disjoint_surgeries(
    vertices: list[Point],
    forest: PacketForest,
) -> tuple[list[Point], list[SurgeryResult]]:
    """Simultaneous surgeries on disjoint disks."""
    current = list(vertices)
    results: list[SurgeryResult] = []
    for disk in surgery_order(forest):
        res = apply_local_surgery(current, disk)
        results.append(res)
        if res.is_jordan:
            current = res.surgered_vertices
    return current, results


def apply_nested_surgeries(
    vertices: list[Point],
    forest: PacketForest,
) -> tuple[list[Point], list[SurgeryResult]]:
    """Use maximal disks only — one surgery removes entire descendant tree."""
    return apply_disjoint_surgeries(vertices, PacketForest(disks=maximal_disks(forest)))
