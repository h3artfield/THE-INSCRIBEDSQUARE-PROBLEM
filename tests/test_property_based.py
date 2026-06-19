"""Property-based and transformation tests."""

from __future__ import annotations

from fractions import Fraction

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.exact_squares.validator import validate_square_certificate

hypothesis = pytest.importorskip("hypothesis")
from hypothesis import given, settings  # noqa: E402
import hypothesis.strategies as st  # noqa: E402

RATIONAL_ROT = (
    (Fraction(3, 5), Fraction(-4, 5)),
    (Fraction(4, 5), Fraction(3, 5)),
)


def _apply_rational_rotation(poly: PolygonCurve) -> PolygonCurve:
    verts = []
    for x, y in poly.vertices:
        nx = RATIONAL_ROT[0][0] * x + RATIONAL_ROT[0][1] * y
        ny = RATIONAL_ROT[1][0] * x + RATIONAL_ROT[1][1] * y
        verts.append((nx, ny))
    return PolygonCurve(verts)


@pytest.mark.fast
def test_rational_rotation_preserves_existence():
    base = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    r = _apply_rational_rotation(base)
    assert len(solve_polygon_full(base).isolated) >= 1
    assert len(solve_polygon_full(r).isolated) >= 1


@pytest.mark.fast
def test_reflection_via_reversal():
    poly = PolygonCurve([(0, 0), (5, 0), (6, 4), (1, 5)])
    a = len(solve_polygon_full(poly).isolated)
    b = len(solve_polygon_full(poly.reversed()).isolated)
    assert a == b


@pytest.mark.fast
@given(st.integers(0, 5), st.integers(0, 5), st.integers(1, 6), st.integers(1, 6))
@settings(max_examples=15, deadline=None)
def test_property_simple_rectangles_have_squares(x, y, w, h):
    if w == h == 0:
        return
    poly = PolygonCurve([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])
    result = solve_polygon_full(poly)
    assert len(result.isolated) >= 1
    for cert in result.isolated:
        assert validate_square_certificate(poly, cert).ok
