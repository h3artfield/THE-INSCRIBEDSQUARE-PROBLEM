"""Reference annular Jordan curve Gamma_ref."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

Point = tuple[float, float]
CurveFn = Callable[[float], Point]


@dataclass
class ReferenceAnnulus:
    r_inner: float
    r_outer: float
    corridor_width: float
    name: str


def _smooth_step(x: float) -> float:
    """C^1 bump 0->1 on [0,1]."""
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def star_annular_gamma(spec: ReferenceAnnulus) -> CurveFn:
    """
    Star-shaped Jordan curve: R(t) alternates inner/outer by quadrant.

    Outer arcs on [0,pi/2] and [pi,3pi/2]; inner on complementary quadrants.
    """
    ri, ro = spec.r_inner, spec.r_outer

    def gamma(t: float) -> Point:
        t = t % (2 * math.pi)
        q = int(t / (math.pi / 2)) % 4
        local = (t % (math.pi / 2)) / (math.pi / 2)
        if q in (0, 2):
            r = ro - (ro - ri) * _smooth_step(local)
        else:
            r = ri + (ro - ri) * _smooth_step(local)
        return r * math.cos(t), r * math.sin(t)

    return gamma


def default_reference_annulus() -> ReferenceAnnulus:
    return ReferenceAnnulus(r_inner=0.45, r_outer=1.0, corridor_width=0.08, name="star_annular")
