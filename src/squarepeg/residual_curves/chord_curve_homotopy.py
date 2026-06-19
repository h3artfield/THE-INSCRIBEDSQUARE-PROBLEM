"""Chord-to-curve homotopy for square equations (Directive 012)."""

from __future__ import annotations

from typing import Callable

from squarepeg.residual_curves.smooth_square_system import Point, SmoothSupport


def chord_point(a: Point, b: Point, u: float) -> Point:
    return ((1 - u) * a[0] + u * b[0], (1 - u) * a[1] + u * b[1])


def homotopy_point(
    lam: float,
    u: float,
    a: Point,
    b: Point,
    support: SmoothSupport,
) -> Point:
    """p^lambda = (1-lambda)*chord + lambda*smooth(u)."""
    chord = chord_point(a, b, u)
    smooth = support.evaluate(u)
    return (
        (1 - lam) * chord[0] + lam * smooth[0],
        (1 - lam) * chord[1] + lam * smooth[1],
    )


def F_lambda(
    params: list[float],
    lam: float,
    chord_endpoints: list[tuple[Point, Point]],
    supports: list[SmoothSupport],
) -> list[float]:
    pts = [
        homotopy_point(lam, params[i], chord_endpoints[i][0], chord_endpoints[i][1], supports[i])
        for i in range(4)
    ]

    def sq(a: Point, b: Point) -> float:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    return [
        sq(pts[0], pts[1]) - sq(pts[1], pts[2]),
        sq(pts[1], pts[2]) - sq(pts[2], pts[3]),
        sq(pts[2], pts[3]) - sq(pts[3], pts[0]),
        sq(pts[0], pts[2]) - sq(pts[1], pts[3]),
    ]
