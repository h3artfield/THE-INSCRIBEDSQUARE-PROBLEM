"""Truncated double-spiral polygons for exact solver experiments."""

from __future__ import annotations

from fractions import Fraction

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.residual_curves.double_spiral import TruncatedDoubleSpiral


def rational_truncated_spiral(turns: int, denom: int = 1000) -> PolygonCurve | None:
    """Build rational PL approximation; returns None if not simple."""
    t = TruncatedDoubleSpiral(turns=turns)
    pts = t.closed_polygon()
    rat = [
        (
            Fraction(p[0]).limit_denominator(denom),
            Fraction(p[1]).limit_denominator(denom),
        )
        for p in pts
    ]
    try:
        return PolygonCurve(rat)
    except ValueError:
        return None
