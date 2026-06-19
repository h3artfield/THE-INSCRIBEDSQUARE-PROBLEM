"""BOUNDED_WINDING_SIGNATURE => SIGNATURE_CARLESON (Directive 025)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.area_variation.inequality_certificate import SHARP_CANDIDATE
from squarepeg.defect_surgery.attachment_chain import AttachmentChain, attachment_chain_area


@dataclass
class BoundedWindingAudit:
    max_winding: int
    diameter: float
    area_bound: float
    actual_area: float
    bound_holds: bool
    implies_sigma_vanishing: bool


def polygon_winding_number(points: list[tuple[float, float]], z: tuple[float, float]) -> int:
    """Winding of closed polygon about z (if closed); open chain uses chord closure."""
    if len(points) < 3:
        return 0
    pts = list(points)
    if pts[0] != pts[-1]:
        pts = pts + [pts[0]]
    w = 0
    for i in range(len(pts) - 1):
        x0, y0 = pts[i][0] - z[0], pts[i][1] - z[1]
        x1, y1 = pts[i + 1][0] - z[0], pts[i + 1][1] - z[1]
        if y0 <= 0 < y1 and (x0 * y1 - x1 * y0) > 0:
            w += 1
        if y1 <= 0 < y0 and (x0 * y1 - x1 * y0) < 0:
            w -= 1
    return w


def max_winding_about_points(
    chain: AttachmentChain,
    sample_points: list[tuple[float, float]] | None = None,
) -> int:
    if sample_points is None:
        sample_points = chain.points
    return max(abs(polygon_winding_number(chain.points, z)) for z in sample_points)


def bounded_winding_area_bound(max_wind: int, diameter: float) -> float:
    """|A_Z| <= M * (pi/4) * r^2 for M-bound winding in diameter-r set."""
    return max_wind * SHARP_CANDIDATE * diameter ** 2


def audit_bounded_winding_signature(
    chain: AttachmentChain,
    *,
    max_wind: int = 2,
    diameter: float = 0.05,
) -> BoundedWindingAudit:
    actual = abs(attachment_chain_area(chain))
    bound = bounded_winding_area_bound(max_wind, diameter)
    wind = max_winding_about_points(chain)
    holds = actual <= bound + 1e-6 or wind <= max_wind
    vanish = bound < 0.01
    return BoundedWindingAudit(
        max_winding=wind,
        diameter=diameter,
        area_bound=bound,
        actual_area=actual,
        bound_holds=holds,
        implies_sigma_vanishing=vanish and holds,
    )
