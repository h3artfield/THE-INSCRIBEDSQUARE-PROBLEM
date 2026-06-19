"""Attachment-chain area for accumulated surgery (Directive 024)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_surgery.concatenation_area import relative_area_path, wedge
from squarepeg.defect_surgery.packet_disk import PacketDisk, Point


@dataclass
class AttachmentChain:
    """Polygonal chain of retained/chord attachment points in traversal order."""
    points: list[Point]
    chord_indices: list[int]  # indices where point is a chord endpoint


@dataclass
class ChainControls:
    mu2: float
    mu1: float
    v_att2_sq: float
    a_att: float


def mu2_on_interval(disks: list[PacketDisk], interval: set[int]) -> float:
    return sum(d.diameter ** 2 for d in disks if _disk_hits(d, interval))


def mu1_on_interval(disks: list[PacketDisk], interval: set[int]) -> float:
    return sum(d.diameter for d in disks if _disk_hits(d, interval))


def _disk_hits(d: PacketDisk, interval: set[int]) -> bool:
    idxs = set(range(min(d.interval_start, d.interval_end), max(d.interval_start, d.interval_end) + 1))
    return bool(idxs & interval)


def v_att2_squared(chain: AttachmentChain) -> float:
    """Sup over partition of sum |z_{k+1}-z_k|^2 — here single partition along chain."""
    pts = chain.points
    if len(pts) < 2:
        return 0.0
    return sum((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2 for i in range(len(pts) - 1))


def attachment_chain_area(chain: AttachmentChain) -> float:
    """A_att(J) from polygonal attachment chain (relative to first point)."""
    if len(chain.points) < 2:
        return 0.0
    return relative_area_path(chain.points)


def chain_controls(disks: list[PacketDisk], chain: AttachmentChain, interval: set[int]) -> ChainControls:
    return ChainControls(
        mu2=mu2_on_interval(disks, interval),
        mu1=mu1_on_interval(disks, interval),
        v_att2_sq=v_att2_squared(chain),
        a_att=attachment_chain_area(chain),
    )


def build_chord_chain_from_disks(
    vertices: list[Point],
    disks: list[PacketDisk],
) -> AttachmentChain:
    """Attachment points a_i, b_i for maximal surgery intervals."""
    pts: list[Point] = []
    chord_idx: list[int] = []
    for d in sorted(disks, key=lambda x: x.interval_start):
        a = vertices[d.interval_start]
        b = vertices[d.interval_end]
        if not pts or pts[-1] != a:
            pts.append(a)
        chord_idx.append(len(pts))
        pts.append(b)
    return AttachmentChain(points=pts, chord_indices=chord_idx)
