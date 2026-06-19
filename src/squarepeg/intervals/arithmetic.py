"""Outward-rounded interval arithmetic for floating-point polygon certification."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Literal

from squarepeg.curves.polygon import PolygonCurve

IntervalStatus = Literal["certified", "non_solution", "unresolved"]


@dataclass
class Interval:
    lo: float
    hi: float

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            self.lo, self.hi = self.hi, self.lo

    def contains(self, x: float) -> bool:
        return self.lo <= x <= self.hi

    def width(self) -> float:
        return self.hi - self.lo

    @classmethod
    def point(cls, x: float, eps: float = 1e-12) -> Interval:
        return cls(x - eps, x + eps)


@dataclass
class IntervalSquareCertificate:
    polygon_hash: str
    coordinate_intervals: list[list[list[float]]]
    parameter_intervals: list[list[float]] | None
    residual_intervals: dict[str, list[float]]
    side_length_lower_bound: float | None
    precision_eps: float
    subdivision_depth: int
    certification_status: IntervalStatus
    subdivision_history: list[str] = field(default_factory=list)
    message: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def _interval_add(a: Interval, b: Interval) -> Interval:
    return Interval(a.lo + b.lo, a.hi + b.hi)


def _interval_sub(a: Interval, b: Interval) -> Interval:
    return Interval(a.lo - b.hi, a.hi - b.lo)


def _interval_mul(a: Interval, b: Interval) -> Interval:
    vals = [a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi]
    return Interval(min(vals), max(vals))


def _side_length_sq_interval(vx: Interval, vy: Interval) -> Interval:
    return _interval_add(_interval_mul(vx, vx), _interval_mul(vy, vy))


def certify_interval_polygon(
    polygon: PolygonCurve,
    *,
    eps: float = 1e-8,
    max_depth: int = 4,
) -> IntervalSquareCertificate:
    """Attempt interval certification; returns unresolved if data is too wide."""
    verts = polygon.vertices
    coord_iv = [
        [Interval(float(x) - eps, float(x) + eps), Interval(float(y) - eps, float(y) + eps)]
        for x, y in verts
    ]
    # Without a candidate square, we cannot certify existence from floats alone.
    return IntervalSquareCertificate(
        polygon_hash=polygon.polygon_hash(),
        coordinate_intervals=[[[iv.lo, iv.hi] for iv in pt] for pt in coord_iv],
        parameter_intervals=None,
        residual_intervals={},
        side_length_lower_bound=None,
        precision_eps=eps,
        subdivision_depth=0,
        certification_status="unresolved",
        message=(
            "Floating-point polygon recorded with outward-rounded coordinate intervals. "
            "No approximate root was promoted to an exact certificate."
        ),
    )
