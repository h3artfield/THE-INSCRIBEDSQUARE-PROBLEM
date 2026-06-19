"""Lobe area allocation L1/L2/L3 (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.area_variation.chord_lobes import Lobe, lobe_diameter, shoelace_abs
from squarepeg.area_variation.polygonal_arc import PolygonalArc
from squarepeg.area_variation.chord_lobes import decompose_lobes_general_position

AllocationMode = Literal["DOMINANT_LOBE", "MANY_LOBE_ACCUMULATION", "LARGE_CANCELLATION"]


@dataclass
class LobeAllocation:
    mode: AllocationMode
    lobes: list[Lobe]
    total_signed: float
    total_abs: float
    dominant_fraction: float


def allocate_lobe_areas(arc: PolygonalArc, epsilon_0: float, c1: float = 0.25) -> LobeAllocation:
    lobes = decompose_lobes_general_position(arc)
    if not lobes:
        return LobeAllocation("DOMINANT_LOBE", [], 0.0, 0.0, 0.0)

    areas = [shoelace_abs(l.closed_vertices()) * l.sign for l in lobes]
    abs_areas = [abs(a) for a in areas]
    total_signed = sum(areas)
    total_abs = sum(abs_areas)
    max_abs = max(abs_areas)
    dom_frac = max_abs / max(abs(total_signed), 1e-12)

    if max_abs >= c1 * epsilon_0:
        mode: AllocationMode = "DOMINANT_LOBE"
    elif total_abs >= epsilon_0 and abs(total_signed) < epsilon_0 / 2:
        mode = "LARGE_CANCELLATION"
    else:
        mode = "MANY_LOBE_ACCUMULATION"

    return LobeAllocation(
        mode=mode,
        lobes=lobes,
        total_signed=total_signed,
        total_abs=total_abs,
        dominant_fraction=dom_frac,
    )
