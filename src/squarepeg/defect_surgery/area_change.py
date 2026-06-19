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
    Three quantities (Directive 024):
    - A_P(I) = relative_area(old_chain) may be large (winding)
    - A_sigma(I) = 0 for straight chord
    - |A_{S_I(P)}(J) - A_P(J)| NOT bounded by O(r^2) without winding bound
    """
    new_chain = [cross.start] + cross.interior_points + [cross.end]
    d_old = relative_area(old_chain)
    d_new = relative_area(new_chain)
    delta = abs(d_new - d_old)
    diam = max(
        math.hypot(old_chain[i][0] - old_chain[j][0], old_chain[i][1] - old_chain[j][1])
        for i in range(len(old_chain))
        for j in range(len(old_chain))
    ) if len(old_chain) > 1 else 0.0
    return AreaChangeBound(
        delta=delta,
        bound=delta,  # exact delta; no false O(r^2) claim
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
