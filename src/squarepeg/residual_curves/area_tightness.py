"""Area-tightness criterion (T022 program)."""

from __future__ import annotations

from typing import Callable, Sequence

from squarepeg.area_variation.signed_area import relative_area_increment
from squarepeg.rough_area.liouville_recovery import recover_primitive

Point = tuple[float, float]


def max_relative_area_on_grid(
    points: Sequence[Point],
    max_pair_distance: float | None = None,
) -> float:
    """sup_{s,t} |A(s,t)| on vertex grid (exploratory)."""
    n = len(points)
    m = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            if max_pair_distance is not None:
                dx = points[j][0] - points[i][0]
                dy = points[j][1] - points[i][1]
                if dx * dx + dy * dy > max_pair_distance * max_pair_distance:
                    continue
            sub = list(points[i : j + 1])
            m = max(m, abs(relative_area_increment(sub)))
    return m


def is_area_tight_on_grid(
    sequences: list[list[Point]],
    deltas: list[float],
    tol: float = 1e-3,
) -> bool:
    """
    Exploratory check: sup_{d(s,t)<=delta} |A_n(s,t)| -> 0 along sequence.
    Uses vertex grid and Euclidean chord distance proxy.
    """
    if len(sequences) != len(deltas):
        raise ValueError("length mismatch")
    for n_idx, (pts, delta) in enumerate(zip(sequences, deltas)):
        if delta <= 0:
            continue
        m = max_relative_area_on_grid(pts, max_pair_distance=delta)
        if n_idx == len(sequences) - 1 and m > tol:
            return False
    return True


def primitive_oscillation(points: Sequence[Point]) -> float:
    prim = recover_primitive(list(points))
    return max(prim) - min(prim) if prim else 0.0
