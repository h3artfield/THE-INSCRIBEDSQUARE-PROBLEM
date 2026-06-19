"""Winding function for dense attachment (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass

Point = tuple[float, float]

ISODIAMETRIC_C = 4.0 / 3.141592653589793


@dataclass
class WindingMass:
    positive_mass: float
    negative_mass: float
    dominant_sign: str
    dominant_fraction: float
    l_infinity_lower: float


@dataclass
class ClosedWalkAudit:
    closing_chord_bounded: bool
    closing_correction: float
    area_closed: float
    area_normalized: float


def close_polygonal_walk(points: list[Point]) -> list[Point]:
    """Close Z_tilde by endpoint chord when necessary."""
    if len(points) < 2:
        return list(points)
    if points[0] != points[-1]:
        return list(points) + [points[0]]
    return list(points)


def polygon_winding_at(points: list[Point], x: Point) -> int:
    """Discrete winding number at grid point x (ray-crossing)."""
    if len(points) < 3:
        return 0
    wx, wy = x
    w = 0
    n = len(points)
    for i in range(n - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if y1 <= wy < y2 or y2 <= wy < y1:
            t = (wy - y1) / (y2 - y1 + 1e-15)
            ix = x1 + t * (x2 - x1)
            if ix > wx:
                w += 1 if y2 > y1 else -1
    return w


def winding_grid(points: list[Point], *, grid_n: int = 16) -> dict[tuple[int, int], int]:
    """Sample w_n on a grid inside [-1,1]^2."""
    closed = close_polygonal_walk(points)
    w: dict[tuple[int, int], int] = {}
    for i in range(grid_n):
        for j in range(grid_n):
            x = -1.0 + 2.0 * i / max(grid_n - 1, 1)
            y = -1.0 + 2.0 * j / max(grid_n - 1, 1)
            w[(i, j)] = polygon_winding_at(closed, (x, y))
    return w


def winding_l_infinity_lower(area_normalized: float, diameter_r: float = 1.0, epsilon_0: float = 0.025) -> float:
    """|w_n|_{L^inf} >= c * |A_{Z_tilde}| with isodiametric constant."""
    return ISODIAMETRIC_C * abs(area_normalized)


def audit_closed_walk(points: list[Point], area_normalized: float) -> ClosedWalkAudit:
    closed = close_polygonal_walk(points)
    from squarepeg.defect_surgery.concatenation_area import relative_area_path

    corr = 0.0
    if len(points) >= 2 and points[0] != points[-1]:
        corr = relative_area_path([points[-1], points[0]])
    area_closed = relative_area_path(closed) if len(closed) >= 3 else 0.0
    bounded = abs(corr) < 0.1 * max(abs(area_normalized), 1e-9)
    return ClosedWalkAudit(
        closing_chord_bounded=bounded,
        closing_correction=corr,
        area_closed=area_closed,
        area_normalized=area_normalized,
    )


def split_winding_mass(w_grid: dict[tuple[int, int], int], cell_area: float = 4.0 / 256) -> WindingMass:
    pos = sum(max(v, 0) * cell_area for v in w_grid.values())
    neg = sum(max(-v, 0) * cell_area for v in w_grid.values())
    dom = "positive" if pos >= neg else "negative"
    total = pos + neg
    frac = max(pos, neg) / total if total > 0 else 0.0
    max_w = max((abs(v) for v in w_grid.values()), default=0)
    return WindingMass(pos, neg, dom, frac, float(max_w))
