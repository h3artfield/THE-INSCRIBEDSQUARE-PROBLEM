"""Falsification examples for packet surgery (Directive 023 Part X)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from squarepeg.defect_surgery.local_surgery import apply_local_surgery
from squarepeg.defect_surgery.packet_disk import PacketDisk, disk_from_interval, validate_isolated_packet

Point = tuple[float, float]


@dataclass
class SurgeryFalsification:
    name: str
    isolation_holds: bool
    surgery_possible: bool
    carleson_holds: bool
    note: str


@dataclass
class FalsificationReport:
    cases: list[SurgeryFalsification] = field(default_factory=list)


def nonisolated_packet_example() -> tuple[list[Point], PacketDisk]:
    """Disk contains two unrelated parameter arcs."""
    verts = [(0, 0), (1, 0), (1, 1), (0.5, 0.5), (0, 1)]
    disk = disk_from_interval(verts, 0, 2, padding=0.2)
    return verts, disk


def dense_overlap_disks() -> list[PacketDisk]:
    base = [(math.cos(i * 0.5), math.sin(i * 0.5)) for i in range(12)]
    disks = [disk_from_interval(base, i, i + 2, padding=0.15) for i in range(0, 8, 2)]
    return disks


def crosscut_obstruction_example() -> tuple[list[Point], PacketDisk]:
    """Bow-tie: straight chord may intersect retained curve."""
    verts = [(0, 0), (2, 0), (1, 0.3), (1, -0.3), (2, 1), (0, 1)]
    disk = disk_from_interval(verts, 1, 3, padding=0.05)
    return verts, disk


def run_surgery_falsifications() -> FalsificationReport:
    report = FalsificationReport()

    v, d = nonisolated_packet_example()
    iso = validate_isolated_packet(v, d)
    report.cases.append(
        SurgeryFalsification(
            name="nonisolated",
            isolation_holds=iso.is_isolated,
            surgery_possible=False,
            carleson_holds=False,
            note="Multiple arcs in one disk breaks isolation",
        )
    )

    dense = dense_overlap_disks()
    from squarepeg.defect_surgery.carleson_mass import mu_D_on_interval

    mass = mu_D_on_interval(dense, set(range(10)))
    report.cases.append(
        SurgeryFalsification(
            name="dense_overlap",
            isolation_holds=True,
            surgery_possible=False,
            carleson_holds=mass < 0.3,
            note=f"mu on small interval = {mass:.3f}",
        )
    )

    v2, d2 = crosscut_obstruction_example()
    res = apply_local_surgery(v2, d2)
    report.cases.append(
        SurgeryFalsification(
            name="crosscut_obstruction",
            isolation_holds=validate_isolated_packet(v2, d2).is_isolated,
            surgery_possible=res.is_jordan,
            carleson_holds=False,
            note="; ".join(res.messages),
        )
    )

    return report
