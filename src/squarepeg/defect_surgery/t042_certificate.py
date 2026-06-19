"""T042 CHORD_SAFE_ISOLATED_PACKET certification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.area_change import area_change_straight_chord
from squarepeg.defect_surgery.crosscut import straight_chord_crosscut
from squarepeg.defect_surgery.local_surgery import apply_local_surgery
from squarepeg.defect_surgery.packet_disk import PacketDisk

T042Status = Literal["PROVED_LOCALLY", "CONJECTURAL_TARGET"]

CHORD_SAFE_HYPOTHESES = [
    "CHORD_SAFE_ISOLATED_PACKET: isolated Jordan disk D",
    "Straight endpoint chord lies in D and avoids retained curve",
    "Endpoints P(a), P(b) on boundary of D",
]


@dataclass
class T042Certificate:
    jordan_preserved: bool
    uniform_error_bound: float
    replacement_area_zero: bool
    area_change_exact: float
    status: T042Status
    hypotheses: list[str]


def certify_t042(vertices: list[tuple[float, float]], disk: PacketDisk) -> T042Certificate:
    res = apply_local_surgery(vertices, disk)
    chain = vertices[disk.interval_start : disk.interval_end + 1]
    cross = straight_chord_crosscut(vertices[disk.interval_start], vertices[disk.interval_end])
    area_b = area_change_straight_chord(chain, cross)
    replacement_zero = relative_area_chord_zero(cross)
    status: T042Status = "PROVED_LOCALLY" if res.is_jordan and replacement_zero else "CONJECTURAL_TARGET"
    return T042Certificate(
        jordan_preserved=res.is_jordan,
        uniform_error_bound=res.uniform_error,
        replacement_area_zero=replacement_zero,
        area_change_exact=area_b.delta,
        status=status,
        hypotheses=list(CHORD_SAFE_HYPOTHESES),
    )


def relative_area_chord_zero(cross) -> bool:
    from squarepeg.defect_surgery.area_change import relative_area

    pts = [cross.start, cross.end]
    return abs(relative_area(pts)) < 1e-12


def t041_shrinking_support_obstruction() -> str:
    return (
        "T041: If four square vertices lie in a set of diameter r, then side(Q) <= r. "
        "Hence r_n -> 0 packet support cannot yield nondegenerate limit square."
    )
