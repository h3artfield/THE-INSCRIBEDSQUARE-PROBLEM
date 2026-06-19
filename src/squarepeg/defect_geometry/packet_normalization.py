"""Packet normalization: diam=1, relative area A(alpha)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.area_variation.signed_area import relative_area_increment

Point = tuple[float, float]


@dataclass
class NormalizedPacket:
    points: list[Point]
    diameter: float
    relative_area: float
    scale_factor: float


def normalize_packet(points: list[Point]) -> NormalizedPacket:
    """Rescale alpha so diam(alpha([0,1])) = 1."""
    if len(points) < 2:
        raise ValueError("need >= 2 points")
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    diam = max(max(xs) - min(xs), max(ys) - min(ys), 1e-12)
    sf = 1.0 / diam
    scaled = [(p[0] * sf, p[1] * sf) for p in points]
    area = relative_area_increment(scaled)
    return NormalizedPacket(
        points=scaled,
        diameter=1.0,
        relative_area=area,
        scale_factor=sf,
    )


def meets_area_threshold(packet: NormalizedPacket, A0: float) -> bool:
    return abs(packet.relative_area) >= A0
