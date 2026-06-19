"""Lobe definition for defect packets (T021 chord-lobe)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from squarepeg.area_variation.chord_lobes import Lobe, lobe_diameter, shoelace_abs

Point = tuple[float, float]


@dataclass
class LobeRecord:
    """Simple Jordan subloop: arc + chord."""

    interval: tuple[float, float]
    arc_vertices: tuple[Point, ...]
    chord: tuple[Point, Point]
    orientation_sign: int  # sigma_L in {-1, +1}
    diameter: float
    enclosed_area: float
    parent_id: str | None = None
    lobe_id: str = ""
    children: list[str] = field(default_factory=list)

    @classmethod
    def from_chord_lobe(cls, lobe: Lobe, interval: tuple[float, float], lobe_id: str) -> LobeRecord:
        verts = lobe.closed_vertices()
        return cls(
            interval=interval,
            arc_vertices=lobe.arc_vertices,
            chord=lobe.chord,
            orientation_sign=lobe.sign,
            diameter=lobe_diameter(lobe),
            enclosed_area=shoelace_abs(verts),
            lobe_id=lobe_id,
        )


def area_fullness(lobe: LobeRecord, beta: float) -> bool:
    """a_L >= beta * d_L^2."""
    return lobe.enclosed_area >= beta * lobe.diameter * lobe.diameter


def scale_ratio(parent: LobeRecord, child: LobeRecord) -> float:
    if parent.diameter <= 0:
        return 0.0
    return child.diameter / parent.diameter
