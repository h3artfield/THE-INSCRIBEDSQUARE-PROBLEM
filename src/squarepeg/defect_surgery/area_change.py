"""Relative area change under packet surgery (Directive 023)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.area_variation.signed_area import relative_area_increment
from squarepeg.defect_surgery.crosscut import Crosscut
from squarepeg.defect_surgery.packet_disk import Point

CaseKind = Literal["disjoint", "subset", "contains", "one_endpoint", "seam_cross"]


@dataclass
class AreaChangeBound:
    delta: float
    bound: float
    case: CaseKind
    C_area: float = 1.0
    C_end: float = 1.0


C_AREA = 1.0
C_CROSS = math.pi / 4.0  # collar crosscut area vs r^2


def relative_area(vertices: list[Point]) -> float:
    return relative_area_increment(vertices)


def area_change_straight_chord(old_chain: list[Point], cross: Crosscut) -> AreaChangeBound:
    """
    Straight chord replacement: same endpoints => relative area of replacement arc is 0.
    """
    new_chain = [cross.start] + cross.interior_points + [cross.end]
    d_old = relative_area(old_chain)
    d_new = relative_area(new_chain)
    r = max(
        math.hypot(p[0], p[1]) for p in old_chain
    ) if old_chain else 0.0
    r = max(r, 1e-12)
    diam = max(math.hypot(old_chain[i][0] - old_chain[j][0], old_chain[i][1] - old_chain[j][1])
               for i in range(len(old_chain)) for j in range(len(old_chain))) if len(old_chain) > 1 else r
    r = diam
    bound = C_AREA * r * r
    return AreaChangeBound(
        delta=abs(d_new - d_old),
        bound=bound,
        case="subset",
        C_area=C_AREA,
    )


def area_change_collar(old_chain: list[Point], cross: Crosscut, r: float) -> AreaChangeBound:
    """Curved collar: explicit O(r^2) bound."""
    b = area_change_straight_chord(old_chain, cross)
    collar_bound = C_CROSS * r * r
    return AreaChangeBound(
        delta=b.delta,
        bound=max(b.bound, collar_bound),
        case="subset",
        C_area=C_CROSS,
    )


def area_unchanged_outside_interval() -> str:
    return "J disjoint from I => A_{S_I(P)}(J) = A_P(J) exactly."
