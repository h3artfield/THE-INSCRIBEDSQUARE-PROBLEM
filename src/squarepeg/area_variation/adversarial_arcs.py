"""Adversarial simple-arc generators for T021 stress tests."""

from __future__ import annotations

import math
import random
from typing import Iterator

from squarepeg.area_variation.inequality_certificate import certify_arc
from squarepeg.area_variation.polygonal_arc import PolygonalArc, Point


def semicircle_arc(n: int = 32) -> PolygonalArc:
    pts = [(math.cos(math.pi * i / n), math.sin(math.pi * i / n)) for i in range(n + 1)]
    return PolygonalArc.from_points(pts)


def spiral_arc(turns: float = 3.0, n: int = 80) -> PolygonalArc:
    pts: list[Point] = []
    for i in range(n + 1):
        t = i / n
        r = 0.1 + 0.9 * t
        ang = 2 * math.pi * turns * t
        pts.append((r * math.cos(ang), r * math.sin(ang)))
    return PolygonalArc.from_points(pts)


def comb_arc(teeth: int = 10, height: float = 0.3) -> PolygonalArc:
    pts: list[Point] = [(0.0, 0.0)]
    for k in range(teeth):
        x0 = k / teeth
        x1 = (k + 0.5) / teeth
        x2 = (k + 1) / teeth
        pts.extend([(x0, 0.0), (x1, height), (x2, 0.0)])
    return PolygonalArc.from_points(pts)


def zigzag_chord_crossing(n: int = 20, amp: float = 0.4) -> PolygonalArc:
    pts: list[Point] = [(0.0, 0.0)]
    for i in range(1, n + 1):
        x = i / n
        y = amp if i % 2 else -amp
        pts.append((x, y))
    pts.append((1.0, 0.0))
    return PolygonalArc.from_points(pts)


def nested_hook(n: int = 15) -> PolygonalArc:
    pts: list[Point] = [(0.0, 0.0), (1.0, 0.0)]
    for k in range(n):
        t = (k + 1) / (n + 1)
        pts.append((t, 0.2 * ((-1) ** k)))
    pts.append((1.0, 0.0))
    return PolygonalArc.from_points(list(dict.fromkeys(pts)))


def random_simple_arc(n: int = 12, seed: int = 0) -> PolygonalArc:
    rng = random.Random(seed)
    pts: list[Point] = [(0.0, 0.0)]
    angle = 0.0
    for _ in range(n):
        angle += rng.uniform(-0.8, 0.8)
        step = rng.uniform(0.05, 0.15)
        x, y = pts[-1]
        pts.append((x + step * math.cos(angle), y + step * math.sin(angle)))
    return PolygonalArc.from_points(pts)


def all_adversarial() -> Iterator[tuple[str, PolygonalArc]]:
    yield "semicircle", semicircle_arc()
    yield "spiral", spiral_arc()
    yield "comb", comb_arc()
    yield "zigzag", zigzag_chord_crossing()
    yield "hook", nested_hook()
    for s in range(20):
        yield f"random_{s}", random_simple_arc(seed=s)


def max_ratio_search() -> tuple[str, float, bool]:
    worst_name = ""
    worst_ratio = 0.0
    all_pass = True
    for name, arc in all_adversarial():
        cert = certify_arc(arc)
        if cert.ratio > worst_ratio:
            worst_ratio = cert.ratio
            worst_name = name
        if not cert.passes:
            all_pass = False
    return worst_name, worst_ratio, all_pass
