"""Lift polygonal paths to second-level data (exploratory)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PolygonalLift:
    points: list[tuple[float, float]]
    partition_times: list[float]


def lift_from_curve(curve_fn, partition: list[float]) -> PolygonalLift:
    pts = [(curve_fn(t)[0], curve_fn(t)[1]) for t in partition]
    return PolygonalLift(points=pts, partition_times=list(partition))
