"""Simple polygon Jordan curve with exact rational coordinates."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from typing import Iterable, Iterator, Sequence, Tuple, Union

Number = Union[int, Fraction, float]
Point = Tuple[Fraction, Fraction]


def _to_fraction(value: Number) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(value).limit_denominator(10**12)
    raise TypeError(f"unsupported coordinate type: {type(value)!r}")


def _to_point(pt: Sequence[Number]) -> Point:
    if len(pt) != 2:
        raise ValueError("point must have two coordinates")
    return (_to_fraction(pt[0]), _to_fraction(pt[1]))


def _cross(o: Point, a: Point, b: Point) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _segments_intersect_proper(
    p1: Point, p2: Point, p3: Point, p4: Point
) -> bool:
    """True if open segments (p1,p2) and (p3,p4) share an interior point."""
    d1 = _cross(p3, p4, p1)
    d2 = _cross(p3, p4, p2)
    d3 = _cross(p1, p2, p3)
    d4 = _cross(p1, p2, p4)
    if (
        ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0))
        and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))
    ):
        return True
    return False


class PolygonCurve:
    """Cyclic simple polygon with optional exact rational vertices."""

    __slots__ = ("_vertices",)

    def __init__(self, vertices: Sequence[Sequence[Number]]) -> None:
        if len(vertices) < 3:
            raise ValueError("polygon requires at least three vertices")
        self._vertices: Tuple[Point, ...] = tuple(_to_point(v) for v in vertices)
        if not self._is_simple():
            raise ValueError("polygon is not simple (self-intersection detected)")

    @property
    def vertices(self) -> Tuple[Point, ...]:
        return self._vertices

    @property
    def num_edges(self) -> int:
        return len(self._vertices)

    def edge(self, index: int) -> Tuple[Point, Point]:
        n = self.num_edges
        i = index % n
        return self._vertices[i], self._vertices[(i + 1) % n]

    def edge_parametric(self, index: int) -> Tuple[Point, Point]:
        """Return (origin, direction) for e(u) = origin + u * direction, u in [0,1]."""
        a, b = self.edge(index)
        return a, (b[0] - a[0], b[1] - a[1])

    def evaluate_edge(self, index: int, u: Fraction) -> Point:
        if u < 0 or u > 1:
            raise ValueError("edge parameter must lie in [0, 1]")
        origin, direction = self.edge_parametric(index)
        return (
            origin[0] + u * direction[0],
            origin[1] + u * direction[1],
        )

    def signed_area(self) -> Fraction:
        area = Fraction(0)
        n = self.num_edges
        for i in range(n):
            x0, y0 = self._vertices[i]
            x1, y1 = self._vertices[(i + 1) % n]
            area += x0 * y1 - x1 * y0
        return area / 2

    def area(self) -> Fraction:
        return abs(self.signed_area())

    def diameter(self) -> Fraction:
        import math

        dsq = float(self.diameter_squared())
        return Fraction(math.sqrt(dsq)).limit_denominator(10**12)

    def diameter_squared(self) -> Fraction:
        best = Fraction(0)
        verts = self._vertices
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                dx = verts[i][0] - verts[j][0]
                dy = verts[i][1] - verts[j][1]
                dist_sq = dx * dx + dy * dy
                if dist_sq > best:
                    best = dist_sq
        return best

    def normalize_orientation(self) -> PolygonCurve:
        """Return ccw-oriented copy (positive signed area)."""
        if self.signed_area() < 0:
            return self.reversed()
        return self

    def translate(self, dx: Number, dy: Number) -> PolygonCurve:
        tx, ty = _to_fraction(dx), _to_fraction(dy)
        return PolygonCurve(
            [(x + tx, y + ty) for x, y in self._vertices]
        )

    def scale(self, factor: Number) -> PolygonCurve:
        s = _to_fraction(factor)
        return PolygonCurve([(x * s, y * s) for x, y in self._vertices])

    def rotate(self, angle_radians: float) -> PolygonCurve:
        c = Fraction(math.cos(angle_radians)).limit_denominator(10**12)
        s = Fraction(math.sin(angle_radians)).limit_denominator(10**12)
        rotated: list[Point] = []
        for x, y in self._vertices:
            rotated.append((x * c - y * s, x * s + y * c))
        return PolygonCurve(rotated)

    def reversed(self) -> PolygonCurve:
        return PolygonCurve(list(reversed(self._vertices)))

    def _is_simple(self) -> bool:
        n = self.num_edges
        edges = [self.edge(i) for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if abs(i - j) <= 1 or (i == 0 and j == n - 1):
                    continue
                if _segments_intersect_proper(edges[i][0], edges[i][1], edges[j][0], edges[j][1]):
                    return False
        return True

    def polygon_hash(self) -> str:
        """Deterministic SHA-256 of normalized vertex data."""
        payload = self.to_canonical_dict()
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def to_canonical_dict(self) -> dict:
        return {
            "vertices": [
                [str(v[0]), str(v[1])] for v in self.normalize_orientation().vertices
            ]
        }

    def to_dict(self) -> dict:
        return {
            "vertices": [[str(v[0]), str(v[1])] for v in self._vertices],
        }

    @classmethod
    def from_dict(cls, data: dict) -> PolygonCurve:
        verts = [(_to_fraction(v[0]), _to_fraction(v[1])) for v in data["vertices"]]
        return cls(verts)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PolygonCurve):
            return NotImplemented
        return self._vertices == other._vertices

    def __repr__(self) -> str:
        return f"PolygonCurve({len(self._vertices)} vertices)"

    def cyclic_order(self, i1: int, i2: int, i3: int, i4: int) -> bool:
        """True if i1,i2,i3,i4 appear in forward order traversing the boundary from i1."""
        n = self.num_edges

        def dist(a: int, b: int) -> int:
            return (b - a) % n

        d2, d3, d4 = dist(i1, i2), dist(i1, i3), dist(i1, i4)
        if d2 == 0 or d3 == 0 or d4 == 0:
            return False
        return 0 < d2 < d3 < d4 < n

    def _is_valid_edge_quadruple(self, i1: int, i2: int, i3: int, i4: int) -> bool:
        if len({i1, i2, i3, i4}) == 4:
            return self.cyclic_order(i1, i2, i3, i4)
        n = self.num_edges
        seq = [i1, i2, i3, i4]
        base = i1
        last_dist = 0
        for e in seq[1:]:
            d = (e - base) % n
            if d == 0:
                continue
            if d <= last_dist and last_dist > 0:
                return False
            last_dist = d
        return True

    def iter_cyclic_edge_quadruples(self, allow_repeated: bool = True) -> Iterator[Tuple[int, int, int, int]]:
        n = self.num_edges
        for i1 in range(n):
            for i2 in range(n):
                for i3 in range(n):
                    for i4 in range(n):
                        if not allow_repeated and len({i1, i2, i3, i4}) < 4:
                            continue
                        if not self._is_valid_edge_quadruple(i1, i2, i3, i4):
                            continue
                        yield (i1, i2, i3, i4)
