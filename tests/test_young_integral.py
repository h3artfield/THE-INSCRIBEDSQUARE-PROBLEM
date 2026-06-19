"""Young integral on polygonal paths."""

from fractions import Fraction

import pytest

from squarepeg.variation.young_integral import (
    classical_area_from_points,
    classical_area_from_points_frac,
    liouville_integrand_xi_dx,
    max_primitive_gap,
    primitive_from_points,
    primitive_from_points_frac,
    young_pairing_bound,
)


@pytest.mark.fast
def test_linear_segment_exact():
    p0 = (Fraction(0), Fraction(0))
    p1 = (Fraction(2), Fraction(2))
    assert liouville_integrand_xi_dx(p0, p1) == Fraction(2)


@pytest.mark.fast
def test_primitive_additivity_frac():
    pts = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), (Fraction(1), Fraction(1))]
    prims = primitive_from_points_frac(pts)
    assert prims[0] == 0
    assert prims[-1] == prims[1]


@pytest.mark.fast
def test_circle_area_matches_green():
    import math

    n = 128
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    area = classical_area_from_points(pts)
    assert abs(area - math.pi) < 0.1


@pytest.mark.fast
def test_young_constant_finite():
    assert 0 < young_pairing_bound(1.5) < 100


@pytest.mark.fast
def test_primitive_convergence_on_refined_circle():
    import math

    def circle(t):
        return (math.cos(2 * math.pi * t), math.sin(2 * math.pi * t))

    def sample(n):
        return [circle(i / n) for i in range(n + 1)]

    p100 = primitive_from_points(sample(100))
    p400 = primitive_from_points(sample(400))
    m = min(len(p100), len(p400))
    # Compare at corresponding indices (different partitions — exploratory).
    assert abs(p100[-1] - p400[-1]) < 0.05


@pytest.mark.fast
def test_max_primitive_gap_zero_identical():
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    p = primitive_from_points(pts)
    assert max_primitive_gap(p, p) == 0.0
