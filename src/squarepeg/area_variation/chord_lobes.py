"""Chord–lobe decomposition for simple polygonal arcs."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.area_variation.polygonal_arc import Point, PolygonalArc
from squarepeg.area_variation.signed_area import lie_bracket_scalar


@dataclass(frozen=True)
class Lobe:
    """Simple closed polygon: arc subpath + chord subsegment."""

    arc_vertices: tuple[Point, ...]
    chord: tuple[Point, Point]
    sign: int  # +1 or -1 winding contribution

    def closed_vertices(self) -> list[Point]:
        a, b = self.chord
        return list(self.arc_vertices) + [b] if self.arc_vertices[-1] != b else list(self.arc_vertices)


def segment_intersection(
    p1: Point, p2: Point, q1: Point, q2: Point, eps: float = 1e-12
) -> tuple[float, float] | None:
    """Proper interior intersection of open segments, or None."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = q1
    x4, y4 = q2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < eps:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
    if eps < t < 1 - eps and eps < u < 1 - eps:
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None


def shoelace_abs(vertices: list[Point]) -> float:
    if len(vertices) < 3:
        return 0.0
    twice = 0.0
    n = len(vertices)
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        twice += x0 * y1 - x1 * y0
    return abs(twice) / 2.0


def lobe_diameter(lobe: Lobe) -> float:
    pts = lobe.closed_vertices()
    m = 0.0
    for i, p in enumerate(pts):
        for q in pts[i + 1 :]:
            m = max(m, math.hypot(p[0] - q[0], p[1] - q[1]))
    return m


def chord_arc_intersections(arc: PolygonalArc) -> list[tuple[int, Point]]:
    """Intersections of closing chord with arc edges (excluding endpoints)."""
    hits: list[tuple[int, Point]] = []
    chord = (arc.start, arc.end)
    for i in range(arc.n_edges):
        p, q = arc.edge(i)
        if i == 0 or i == arc.n_edges - 1:
            continue
        hit = segment_intersection(p, q, chord[0], chord[1])
        if hit is not None:
            hits.append((i, hit))
    return hits


def decompose_lobes_general_position(arc: PolygonalArc) -> list[Lobe]:
    """
    Decompose alpha U chord into lobes when chord meets arc transversely.

    Exploratory: single-lobe when no interior intersections; multi-lobe via
    splitting at intersection points on the arc.
    """
    hits = chord_arc_intersections(arc)
    if not hits:
        return [
            Lobe(
                arc_vertices=arc.vertices,
                chord=(arc.end, arc.start),
                sign=1,
            )
        ]
    # Sort by edge index along arc
    hits.sort(key=lambda x: x[0])
    lobes: list[Lobe] = []
    verts = list(arc.vertices)
    split_pts = [verts[0]]
    for _, pt in hits:
        split_pts.append(pt)
    split_pts.append(verts[-1])
    for i in range(len(split_pts) - 1):
        if split_pts[i] == split_pts[i + 1]:
            continue
        sub = (split_pts[i], split_pts[i + 1]) if len(split_pts) == 2 else None
        if sub:
            lobes.append(Lobe(arc_vertices=(split_pts[i], split_pts[i + 1]), chord=(split_pts[i + 1], split_pts[i]), sign=(-1) ** i))
    if lobes:
        return lobes
    return [Lobe(arc_vertices=arc.vertices, chord=(arc.end, arc.start), sign=1)]


def isodiametric_bound(area: float, diam: float) -> bool:
    """Area <= (pi/4) * diam^2."""
    return area <= (math.pi / 4.0) * diam * diam + 1e-9
