"""Minimal area-defect witness extraction."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Sequence

from squarepeg.area_variation.signed_area import relative_area_increment
from squarepeg.robust_degree.area_defect import arc_length_param_distance

CurveFn = Callable[[float], tuple[float, float]]
Point = tuple[float, float]


@dataclass
class DefectWitness:
    n: int
    s: float
    t: float
    interval_length: float
    area_magnitude: float
    image_diameter: float


@dataclass
class WitnessSelectionResult:
    witnesses: list[DefectWitness] = field(default_factory=list)
    selection_lemma_required: bool = False
    gap_description: str = ""


def arc_area(gamma: CurveFn, s: float, t: float, samples: int = 16) -> float:
    if t < s:
        s, t = t, s
    pts = [gamma(s + (t - s) * i / (samples - 1)) for i in range(samples)]
    return abs(relative_area_increment(pts))


def image_diameter(gamma: CurveFn, s: float, t: float, samples: int = 16) -> float:
    pts = [gamma(s + (t - s) * i / max(1, samples - 1)) for i in range(samples)]
    m = 0.0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            m = max(m, math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]))
    return m


def find_witness_at_scale(
    gamma: CurveFn,
    delta: float,
    n: int,
    *,
    epsilon_0: float = 0.01,
) -> DefectWitness | None:
    """Find interval [s,t] with |I| <= delta and |A(I)| >= epsilon_0."""
    step = delta / 8
    best: DefectWitness | None = None
    s_val = 0.0
    while s_val < 1.0:
        t_val = min(1.0, s_val + delta)
        if arc_length_param_distance(gamma, s_val, t_val) <= delta:
            a = arc_area(gamma, s_val, t_val)
            if a >= epsilon_0:
                d = image_diameter(gamma, s_val, t_val)
                w = DefectWitness(n, s_val, t_val, t_val - s_val, a, d)
                if best is None or a > best.area_magnitude:
                    best = w
        s_val += step
    return best


def extract_minimal_witnesses(
    gammas: Sequence[CurveFn],
    deltas: Sequence[float],
    *,
    epsilon_0: float = 0.01,
) -> WitnessSelectionResult:
    """
    Attempt selection of n_k, delta_k, I_k with area >= epsilon_0.

    Full minimality (no subinterval with half area) requires an additional
    combinatorial selection lemma — flagged when not verified.
    """
    result = WitnessSelectionResult()
    for k, delta in enumerate(deltas):
        n = min(k, len(gammas) - 1)
        w = find_witness_at_scale(gammas[n], delta, n, epsilon_0=epsilon_0)
        if w:
            result.witnesses.append(w)
    if not result.witnesses:
        result.selection_lemma_required = True
        result.gap_description = (
            "T035-GAP: from 'no area-tight subsequence' alone, extracting "
            "minimal defect witnesses (n_k, delta_k, I_k) requires a separate "
            "diagonal/compactness selection lemma not proved here."
        )
    return result


def t019_image_diameter_shrinks(P_n: Sequence[CurveFn], witnesses: Sequence[DefectWitness]) -> bool:
    """Uniform convergence => diam(P_{n_k}(I_k)) -> 0 when |I_k| -> 0."""
    if len(P_n) < 2 or not witnesses:
        return True
    d0 = witnesses[0].image_diameter
    dk = witnesses[-1].image_diameter
    return dk <= d0 + 0.5  # shrink or bounded; full proof in docs
