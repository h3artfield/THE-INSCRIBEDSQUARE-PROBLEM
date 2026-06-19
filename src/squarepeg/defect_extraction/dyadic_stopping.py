"""Dyadic bad-interval stopping with Chen endpoint corrections (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from squarepeg.robust_degree.minimal_defect_interval import (
    DefectInterval,
    DyadicMinimalInterval,
    arc_area_with_chord,
    dyadic_minimize,
    endpoint_chord_correction,
)

CurveFn = Callable[[float], tuple[float, float]]


@dataclass
class BadInterval:
    s: float
    t: float
    area: float
    minimal: bool
    endpoint_correction: float


def is_bad_interval(gamma: CurveFn, s: float, t: float, epsilon_0: float) -> bool:
    return arc_area_with_chord(gamma, s, t) >= epsilon_0 / 4


def minimal_bad_interval(
    gamma: CurveFn,
    interval: DefectInterval,
    epsilon_0: float,
) -> BadInterval:
    """Minimal bad: bad but neither dyadic child bad (with endpoint correction)."""
    dm = dyadic_minimize(gamma, interval, epsilon_0)
    return BadInterval(
        s=dm.interval.s,
        t=dm.interval.t,
        area=dm.interval.area,
        minimal=dm.children_max_area < epsilon_0 / 4,
        endpoint_correction=dm.endpoint_correction,
    )


def chen_child_signature(gamma: CurveFn, s: float, t: float) -> tuple[float, float, float]:
    """Parent area, sum child areas, endpoint correction."""
    mid = 0.5 * (s + t)
    a_p = arc_area_with_chord(gamma, s, t)
    a_l = arc_area_with_chord(gamma, s, mid)
    a_r = arc_area_with_chord(gamma, mid, t)
    corr = endpoint_chord_correction(gamma, s, t)
    return a_p, a_l + a_r, corr
