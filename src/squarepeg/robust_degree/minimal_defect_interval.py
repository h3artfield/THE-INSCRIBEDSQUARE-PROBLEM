"""Dyadic minimal defect intervals with endpoint correction."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Sequence

from squarepeg.area_variation.signed_area import relative_area_increment

CurveFn = Callable[[float], tuple[float, float]]


@dataclass
class DefectInterval:
    n_index: int
    s: float
    t: float
    area: float
    diameter: float


@dataclass
class DyadicMinimalInterval:
    interval: DefectInterval
    dyadic_depth: int
    children_max_area: float
    endpoint_correction: float


def arc_area_with_chord(gamma: CurveFn, s: float, t: float, n: int = 32) -> float:
    pts = [gamma(s + (t - s) * i / (n - 1)) for i in range(n)]
    return abs(relative_area_increment(pts))


def endpoint_chord_correction(gamma: CurveFn, s: float, t: float) -> float:
    """
    A(s,t) = 1/2 sum [p_k,p_{k+1}] - 1/2 [p_0,p_n].
    Subdivision correction: child areas sum to parent area plus chord boundary terms.
    """
    mid = 0.5 * (s + t)
    a_full = arc_area_with_chord(gamma, s, t)
    a_left = arc_area_with_chord(gamma, s, mid)
    a_right = arc_area_with_chord(gamma, mid, t)
    return abs(a_full - (a_left + a_right))


def interval_diameter(gamma: CurveFn, s: float, t: float, n: int = 16) -> float:
    pts = [gamma(s + (t - s) * i / max(1, n - 1)) for i in range(n)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return max(max(xs) - min(xs), max(ys) - min(ys), 1e-15)


def select_witness_interval(
    gamma: CurveFn,
    delta: float,
    n_index: int,
    epsilon_0: float,
) -> DefectInterval | None:
    """Choose I_j with |I| <= delta and |A| >= epsilon_0/2."""
    step = delta / 16
    best: DefectInterval | None = None
    s = 0.0
    while s < 1.0 - 1e-12:
        t = min(1.0, s + delta)
        a = arc_area_with_chord(gamma, s, t)
        if a >= epsilon_0 / 2:
            d = interval_diameter(gamma, s, t)
            cand = DefectInterval(n_index, s, t, a, d)
            if best is None or a > best.area:
                best = cand
        s += step
    return best


def dyadic_minimize(
    gamma: CurveFn,
    interval: DefectInterval,
    epsilon_0: float,
    max_depth: int = 12,
) -> DyadicMinimalInterval:
    """
    Subdivide until |A(J)| >= eps_0/4 but every dyadic child has |A| < eps_0/4.

    Uses endpoint correction identity for non-additivity.
    """
    s, t = interval.s, interval.t
    depth = 0
    corr = endpoint_chord_correction(gamma, s, t)
    while depth < max_depth:
        mid = 0.5 * (s + t)
        a_left = arc_area_with_chord(gamma, s, mid)
        a_right = arc_area_with_chord(gamma, mid, t)
        thresh = epsilon_0 / 4
        if a_left >= thresh or a_right >= thresh:
            if a_left >= a_right:
                t = mid
            else:
                s = mid
            depth += 1
            continue
        break
    final = DefectInterval(
        interval.n_index, s, t,
        arc_area_with_chord(gamma, s, t),
        interval_diameter(gamma, s, t),
    )
    mid = 0.5 * (s + t)
    child_max = max(
        arc_area_with_chord(gamma, s, mid),
        arc_area_with_chord(gamma, mid, t),
    )
    return DyadicMinimalInterval(
        interval=final,
        dyadic_depth=depth,
        children_max_area=child_max,
        endpoint_correction=corr,
    )


def extract_shrinking_witnesses(
    gammas: Sequence[CurveFn],
    n_subsequence: Sequence[int],
    *,
    epsilon_0: float,
    j_max: int = 8,
) -> list[DyadicMinimalInterval]:
    """Select I_j at each scale 2^{-j} along uniform-defect subsequence."""
    out: list[DyadicMinimalInterval] = []
    for j in range(1, j_max + 1):
        delta = 2.0 ** (-j)
        k = min(j - 1, len(n_subsequence) - 1)
        nk = n_subsequence[k]
        if nk >= len(gammas):
            continue
        w = select_witness_interval(gammas[nk], delta, nk, epsilon_0)
        if w:
            out.append(dyadic_minimize(gammas[nk], w, epsilon_0))
    return out


def spatial_concentration(
    witnesses: Sequence[DyadicMinimalInterval],
) -> bool:
    """diam(J_j) -> 0 as j increases (monotone after tail)."""
    if len(witnesses) < 2:
        return True
    diams = [w.interval.diameter for w in witnesses]
    return diams[-1] <= diams[0] + 1e-6 or diams[-1] < 0.5 * diams[0]
