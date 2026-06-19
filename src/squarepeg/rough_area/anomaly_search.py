"""Heuristic area-anomaly search sketches (not proofs)."""

from __future__ import annotations


def comb_ribbon_points(n_teeth: int, height: float, width: float) -> list[tuple[float, float]]:
    """Simple comb polyline (open); not closed Jordan — exploratory only."""
    pts: list[tuple[float, float]] = [(0.0, 0.0)]
    x = 0.0
    for i in range(n_teeth):
        pts.append((x, height))
        x += width
        pts.append((x, 0.0))
        x += width
    return pts
