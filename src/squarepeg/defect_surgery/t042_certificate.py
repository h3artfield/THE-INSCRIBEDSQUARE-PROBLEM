"""T042 local packet surgery certification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.area_change import area_change_straight_chord
from squarepeg.defect_surgery.crosscut import straight_chord_crosscut
from squarepeg.defect_surgery.local_surgery import apply_local_surgery
from squarepeg.defect_surgery.packet_disk import PacketDisk

T042Status = Literal["PROVED_LOCALLY", "CONJECTURAL_TARGET"]


@dataclass
class T042Certificate:
    jordan_preserved: bool
    uniform_error_bound: float
    area_bound: float
    status: T042Status


def certify_t042(vertices: list[tuple[float, float]], disk: PacketDisk) -> T042Certificate:
    res = apply_local_surgery(vertices, disk)
    chain = vertices[disk.interval_start : disk.interval_end + 1]
    cross = straight_chord_crosscut(vertices[disk.interval_start], vertices[disk.interval_end])
    area_b = area_change_straight_chord(chain, cross)
    status: T042Status = "PROVED_LOCALLY" if res.is_jordan and area_b.delta <= area_b.bound else "CONJECTURAL_TARGET"
    return T042Certificate(
        jordan_preserved=res.is_jordan,
        uniform_error_bound=res.uniform_error,
        area_bound=area_b.bound,
        status=status,
    )


def t041_shrinking_support_obstruction() -> str:
    return (
        "T041: If four square vertices lie in a set of diameter r, then side(Q) <= r. "
        "Hence r_n -> 0 packet support cannot yield nondegenerate limit square."
    )
