"""Canonical square equation assembly for production solver."""

from __future__ import annotations

from fractions import Fraction
from typing import Literal

from squarepeg.curves.polygon import Point, PolygonCurve

Rotation = Literal["ccw", "cw"]


def _rotation_matrix(kind: Rotation) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    if kind == "ccw":
        return ((Fraction(0), Fraction(-1)), (Fraction(1), Fraction(0)))
    return ((Fraction(0), Fraction(1)), (Fraction(-1), Fraction(0)))


def build_square_system(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> tuple[list[list[Fraction]], list[Fraction]]:
    j = _rotation_matrix(rotation)
    origins: list[Point] = []
    directions: list[Point] = []
    for idx in edges:
        o, d = polygon.edge_parametric(idx)
        origins.append(o)
        directions.append(d)

    rows: list[list[Fraction]] = []
    rhs: list[Fraction] = []

    for comp in range(2):
        row = [Fraction(0)] * 6
        row[0] = -directions[0][comp]
        row[1] = directions[1][comp]
        row[4 + comp] = Fraction(-1)
        rows.append(row)
        rhs.append(origins[0][comp] - origins[1][comp])

    ij = (
        (Fraction(1) + j[0][0], j[0][1]),
        (j[1][0], Fraction(1) + j[1][1]),
    )
    for comp in range(2):
        row = [Fraction(0)] * 6
        row[0] = -directions[0][comp]
        row[2] = directions[2][comp]
        row[4] = -ij[comp][0]
        row[5] = -ij[comp][1]
        rows.append(row)
        rhs.append(origins[0][comp] - origins[2][comp])

    for comp in range(2):
        row = [Fraction(0)] * 6
        row[0] = -directions[0][comp]
        row[3] = directions[3][comp]
        row[4] = -j[comp][0]
        row[5] = -j[comp][1]
        rows.append(row)
        rhs.append(origins[0][comp] - origins[3][comp])

    return rows, rhs
