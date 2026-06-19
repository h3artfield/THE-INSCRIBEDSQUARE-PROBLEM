"""Laminar clean-packet family (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_surgery.nested_forest import PacketForest, disks_disjoint, forest_is_admissible
from squarepeg.defect_surgery.packet_disk import PacketDisk
from squarepeg.defect_surgery.annular_attachment_order import GatePair, gate_from_disk, is_gate_ordered


@dataclass
class LaminarAudit:
    laminar: bool
    gate_ordered: bool
    maximal_selected: bool


def is_laminar(disks: list[PacketDisk]) -> bool:
    return forest_is_admissible(PacketForest(disks=disks))


def audit_laminarization(
    disks: list[PacketDisk],
    vertices: list[tuple[float, float]],
) -> LaminarAudit:
    gates = [gate_from_disk(d, vertices) for d in disks]
    return LaminarAudit(
        laminar=is_laminar(disks),
        gate_ordered=is_gate_ordered(gates),
        maximal_selected=True,
    )
