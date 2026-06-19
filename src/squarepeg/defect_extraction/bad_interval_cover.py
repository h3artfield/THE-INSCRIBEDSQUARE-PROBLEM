"""Maximal bad-interval cover (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from squarepeg.defect_extraction.dyadic_stopping import BadInterval, is_bad_interval, minimal_bad_interval
from squarepeg.robust_degree.minimal_defect_interval import DefectInterval, interval_diameter, select_witness_interval

CurveFn = Callable[[float], tuple[float, float]]


@dataclass
class BadIntervalCover:
    intervals: list[BadInterval]
    residual_bound: float
    maximal_disjoint: bool


def _overlap(a: BadInterval, b: BadInterval) -> bool:
    return not (a.t <= b.s or b.t <= a.s)


def maximal_bad_cover(
    gamma: CurveFn,
    delta: float,
    epsilon_0: float,
    n_index: int = 0,
) -> BadIntervalCover:
    """Greedy maximal interior-disjoint bad intervals at scale delta."""
    step = delta / 8
    candidates: list[BadInterval] = []
    s = 0.0
    while s < 1.0 - 1e-12:
        t = min(1.0, s + delta)
        if is_bad_interval(gamma, s, t, epsilon_0):
            wit = select_witness_interval(gamma, delta, n_index, epsilon_0)
            if wit:
                mb = minimal_bad_interval(gamma, wit, epsilon_0)
                if mb.minimal:
                    candidates.append(mb)
        s += step

    selected: list[BadInterval] = []
    for c in sorted(candidates, key=lambda x: -x.area):
        if all(not _overlap(c, x) for x in selected):
            selected.append(c)

    residual = epsilon_0 / 8
    return BadIntervalCover(
        intervals=selected,
        residual_bound=residual,
        maximal_disjoint=True,
    )


def spatial_diameter(gamma: CurveFn, bi: BadInterval) -> float:
    return interval_diameter(gamma, bi.s, bi.t)
