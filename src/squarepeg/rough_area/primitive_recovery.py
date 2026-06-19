"""Recover Liouville primitive from second-level data (formula reference)."""

from __future__ import annotations

from squarepeg.rough_area.second_level import liouville_from_second_level_symmetric


def recover_liouville_pl(points) -> list[float]:
    """Cumulative int xi dx along PL path; f(0)=0."""
    if not points:
        return []
    vals = [0.0]
    acc = 0.0
    for i in range(len(points) - 1):
        x0, xi0 = points[i]
        x1, xi1 = points[i + 1]
        acc += 0.5 * (xi0 + xi1) * (x1 - x0)
        vals.append(acc)
    return vals


def closed_period_integral(points) -> float:
    prims = recover_liouville_pl(points)
    return prims[-1] - prims[0] if prims else 0.0
