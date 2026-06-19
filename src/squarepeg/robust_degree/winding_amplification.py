"""Winding amplification for defect packets."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

CurveFn = Callable[[float], tuple[float, float]]
Point = tuple[float, float]


@dataclass
class WindingPacket:
    r_j: float
    area_abs: float
    winding_lower_bound: float
    closed_curve_points: list[Point]


def close_by_chord(gamma: CurveFn, s: float, t: float, n: int = 32) -> list[Point]:
    pts = [gamma(s + (t - s) * i / (n - 1)) for i in range(n)]
    return pts + [pts[0]]


def shoelace_winding_bound(points: Sequence[Point]) -> float:
    """Lower bound on sup |wind| from enclosed area / pi r^2."""
    if len(points) < 3:
        return 0.0
    twice = 0.0
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        twice += x0 * y1 - x1 * y0
    area = abs(twice) / 2.0
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    r = max(max(xs) - min(xs), max(ys) - min(ys), 1e-12) / 2.0
    # Curve in disk radius r => |wind| >= area / (pi r^2) for positive loop
    return area / (math.pi * r * r)


def winding_amplification(
    gamma: CurveFn,
    s: float,
    t: float,
    area_abs: float,
    r_j: float,
    *,
    c: float = 1.0 / math.pi,
) -> WindingPacket:
    """
    sup_z |wind(eta_j, z)| >= c * epsilon_0 / r_j^2 -> infinity as r_j -> 0.

    Uses A(eta) = int wind(eta,z) dA and curve contained in disk of radius r_j.
    """
    closed = close_by_chord(gamma, s, t)
    r = max(r_j, 1e-12)
    wind_lb = c * area_abs / (r * r)
    return WindingPacket(r_j=r, area_abs=area_abs, winding_lower_bound=wind_lb, closed_curve_points=closed)


def amplification_diverges(r_j: float, area_abs: float, c: float = 1.0 / math.pi) -> bool:
    return c * area_abs / (max(r_j, 1e-12) ** 2) > 1.0
