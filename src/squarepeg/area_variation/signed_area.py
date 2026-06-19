"""Relative signed area for polygonal arcs (T021)."""

from __future__ import annotations

from fractions import Fraction

from squarepeg.area_variation.polygonal_arc import Point, PolygonalArc

FracPoint = tuple[Fraction, Fraction]


def lie_bracket_scalar(p0: Point, p1: Point) -> float:
    x0, y0 = p0
    x1, y1 = p1
    return x0 * y1 - y0 * x1


def relative_area_increment(points: list[Point]) -> float:
    """
    A_alpha(s,t) = 1/2 sum_k [p_k, p_{k+1}] - 1/2 [p_0, p_n]
    (Yang / AI antisymmetric scalar on arc).
    """
    if len(points) < 2:
        return 0.0
    acc = 0.0
    for i in range(len(points) - 1):
        acc += lie_bracket_scalar(points[i], points[i + 1])
    return 0.5 * acc - 0.5 * lie_bracket_scalar(points[0], points[-1])


def relative_area_arc(arc: PolygonalArc) -> float:
    return relative_area_increment(list(arc.vertices))


def chord_closed_shoelace(arc: PolygonalArc) -> float:
    """
    Signed area of closed walk: arc then closing chord (end -> start).

    Equivalent to relative_area_arc for simple closed walks without self-crossing
    on the chord; for self-crossing, equals winding-weighted lobe sum.
    """
    pts = list(arc.vertices)
    twice = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n] if i < n - 1 else arc.start
        if i == n - 1:
            x1, y1 = arc.start
        twice += x0 * y1 - x1 * y0
    # last edge is end -> start (chord)
    xe, ye = arc.end
    xs, ys = arc.start
    twice += xe * ys - xs * ye
    return twice / 2.0


def relative_area_exact_frac(vertices: list[FracPoint]) -> Fraction:
    if len(vertices) < 2:
        return Fraction(0)
    acc = Fraction(0)
    for i in range(len(vertices) - 1):
        x0, y0 = vertices[i]
        x1, y1 = vertices[i + 1]
        acc += x0 * y1 - y0 * x1
    x0, y0 = vertices[0]
    x1, y1 = vertices[-1]
    return (acc - (x0 * y1 - y0 * x1)) / 2
