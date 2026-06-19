"""Tests for PolygonCurve."""

from fractions import Fraction

import pytest

from squarepeg.curves.polygon import PolygonCurve

pytestmark = pytest.mark.fast


def test_unit_square_area_and_diameter():
    sq = PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert sq.area() == Fraction(1)
    assert sq.signed_area() == Fraction(1)
    dsq = sq.diameter_squared()
    assert dsq == Fraction(2)


def test_orientation_normalization():
    cw = PolygonCurve([(0, 0), (0, 1), (1, 1), (1, 0)])
    ccw = cw.normalize_orientation()
    assert ccw.signed_area() > 0


def test_transformations():
    base = PolygonCurve([(0, 0), (2, 0), (2, 2), (0, 2)])
    t = base.translate(1, 1)
    assert t.vertices[0] == (Fraction(1), Fraction(1))
    s = base.scale(Fraction(1, 2))
    assert s.area() == Fraction(1)
    r = base.reversed()
    assert r.vertices[0] == (Fraction(0), Fraction(2))


def test_serialization_hash_stable():
    p1 = PolygonCurve([(0, 0), (3, 0), (3, 4), (0, 4)])
    p2 = PolygonCurve.from_dict(p1.to_dict())
    assert p1.polygon_hash() == p2.polygon_hash()


def test_triangle_simple():
    tri = PolygonCurve([(0, 0), (1, 0), (0, 1)])
    assert tri.num_edges == 3


def test_self_intersecting_rejected():
    with pytest.raises(ValueError, match="not simple"):
        PolygonCurve([(0, 0), (2, 2), (2, 0), (0, 2)])


def test_rational_coordinates():
    p = PolygonCurve([(0, 0), (Fraction(1, 2), 0), (Fraction(1, 2), Fraction(1, 2)), (0, Fraction(1, 2))])
    assert p.area() == Fraction(1, 4)
