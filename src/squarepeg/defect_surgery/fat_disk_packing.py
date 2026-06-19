"""Fat-disk packing estimate (Directive 024)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_surgery.packet_disk import PacketDisk, dist


@dataclass
class FatDiskPackingAudit:
    c_fat: float
    R: float
    sum_diam_sq: float
    packing_bound: float
    satisfied: bool


def fatness(disk: PacketDisk) -> float:
    """Area / diam^2 proxy: disk area ~ pi r^2, diam=2r => pi/4."""
    return math.pi / 4.0


def packing_estimate_sum_diam_sq(
    disks: list[PacketDisk],
    center: tuple[float, float],
    R: float,
    c_fat: float = math.pi / 4.0,
) -> FatDiskPackingAudit:
    """
    Sum diam^2 over disks in ball B(z,R) <= C(c_fat) R^2 for disjoint fat disks.
    """
    inside = [d for d in disks if dist(d.center, center) + d.radius <= R + 1e-9]
    s = sum(d.diameter ** 2 for d in inside)
    C = 4.0 / max(c_fat, 1e-9)
    bound = C * R * R
    return FatDiskPackingAudit(
        c_fat=c_fat,
        R=R,
        sum_diam_sq=s,
        packing_bound=bound,
        satisfied=s <= bound + 1e-6,
    )
