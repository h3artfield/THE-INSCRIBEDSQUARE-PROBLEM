"""Degree-collapse blow-up analysis (local T032 prototype)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence

Point = tuple[float, float]


@dataclass
class BlowUpScale:
    name: str
    r_n: float
    z_n: Point


@dataclass
class BlowUpRecord:
    scale: BlowUpScale
    rescaled_side: float
    rescaled_area_defect: float
    protected_at_scale: bool
    area_defect_vanishing: bool
    notes: list[str] = field(default_factory=list)


def choose_blowup_scale(
    side_length: float,
    separation: float,
    boundary_margin: float,
) -> BlowUpScale:
    """Cause-specific scale r_n = min positive characteristic scale."""
    candidates = [
        ("side", side_length),
        ("separation", separation),
        ("boundary_margin", boundary_margin),
    ]
    name, r = min((c for c in candidates if c[1] > 0), key=lambda x: x[1], default=("unit", 1.0))
    return BlowUpScale(name=name, r_n=r, z_n=(0.0, 0.0))


def rescale_point(z: Point, z_n: Point, r_n: float) -> Point:
    if r_n <= 0:
        return z
    return ((z[0] - z_n[0]) / r_n, (z[1] - z_n[1]) / r_n)


def rescale_curve(pieces: Sequence[Sequence[Point]], z_n: Point, r_n: float) -> list[list[Point]]:
    return [[rescale_point(p, z_n, r_n) for p in piece] for piece in pieces]


def analyze_blowup(
    side: float,
    separation: float,
    margin: float,
    area_defect: float,
    *,
    protected_rescaled: bool = False,
) -> BlowUpRecord:
    scale = choose_blowup_scale(side, separation, margin)
    rescaled_side = side / scale.r_n if scale.r_n > 0 else 0.0
    rescaled_area = area_defect / (scale.r_n ** 2) if scale.r_n > 0 else 0.0
    notes = []
    if protected_rescaled or rescaled_side > 0.1:
        notes.append("protected square at rescaled level")
    vanish = rescaled_area < 0.01
    if vanish:
        notes.append("vanishing relative-area defect on bounded window")
    return BlowUpRecord(
        scale=scale,
        rescaled_side=rescaled_side,
        rescaled_area_defect=rescaled_area,
        protected_at_scale=protected_rescaled or rescaled_side > 0.1,
        area_defect_vanishing=vanish,
        notes=notes,
    )


def local_dichotomy_prototype(record: BlowUpRecord) -> str:
    """Local prototype: protected at scale OR vanishing area defect."""
    if record.protected_at_scale:
        return "branch_1_protected_at_scale"
    if record.area_defect_vanishing:
        return "branch_2_vanishing_area_defect"
    return "unclassified"
