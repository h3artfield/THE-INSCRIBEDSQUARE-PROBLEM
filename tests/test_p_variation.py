"""p-variation tests."""

from fractions import Fraction

import pytest

from squarepeg.variation.p_variation import (
    osc,
    p_variation,
    p_variation_frac,
    q_variation_from_p_bound,
    total_variation,
)


def _circle(n: int = 64) -> list[tuple[Fraction, Fraction]]:
    import math

    return [
        (
            Fraction(math.cos(2 * math.pi * i / n)).limit_denominator(10**6),
            Fraction(math.sin(2 * math.pi * i / n)).limit_denominator(10**6),
        )
        for i in range(n + 1)
    ]


@pytest.mark.fast
def test_circle_finite_p_variation():
    pts = _circle()
    assert p_variation_frac(pts, 1.5) > 0
    assert p_variation_frac(pts, 1.0) > 3


@pytest.mark.fast
def test_segment_variation_positive():
    pts = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), (Fraction(1), Fraction(1))]
    assert p_variation_frac(pts, 2.0) > 0


@pytest.mark.fast
def test_interpolation_inequality_two_point_path():
    """Sharp constant C=1 on a single jump."""
    p, q = 1.5, 1.75
    pts = [(0.0, 0.0), (1.0, 0.0)]
    left = p_variation(pts, q)
    right = q_variation_from_p_bound(p, q, p_variation(pts, p), osc(pts))
    assert left <= right + 1e-12


@pytest.mark.fast
def test_reparam_invariance_same_breakpoints():
    pts = [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0)]
    assert abs(p_variation(pts, 1.5) - p_variation(pts[:2] + pts[1:], 1.5)) < 1e-12
