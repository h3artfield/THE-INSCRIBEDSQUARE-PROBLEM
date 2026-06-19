"""Example polygons for surgery tests."""

from __future__ import annotations

from squarepeg.defect_surgery.packet_disk import PacketDisk

Point = tuple[float, float]


def example_bump_polygon() -> list[Point]:
    """Square with isolated inward bump on bottom edge (T042 certified)."""
    return [(0, 0), (1, 0), (1.5, 0.35), (2, 0), (3, 0), (3, 3), (0, 3)]


def example_bump_disk() -> PacketDisk:
    return PacketDisk(center=(1.5, 0.0), radius=0.5, interval_start=1, interval_end=3)
