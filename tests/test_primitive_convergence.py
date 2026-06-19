"""Primitive convergence along C1 approximants (formula validation)."""

import math

import pytest

from squarepeg.variation.polygonal_approximation import circle_param, dyadic_partitions, piecewise_linear_interpolation
from squarepeg.variation.p_variation import path_difference, p_variation
from squarepeg.variation.smoothing import round_corners_c1
from squarepeg.variation.young_integral import max_primitive_gap, primitive_from_points


@pytest.mark.fast
def test_pl_to_smooth_primitive_gap_small():
    part = [i / 64 for i in range(65)]
    pl = piecewise_linear_interpolation(circle_param, part)
    sm = round_corners_c1(pl.interpolant, epsilon=0.02)
    from squarepeg.variation.cubic_corner_smoothing import _resample_polyline

    n = 64
    p = _resample_polyline(pl.interpolant, n)
    s = _resample_polyline(sm.smoothed, n)
    fp = primitive_from_points(p)
    fs = primitive_from_points(s)
    assert max_primitive_gap(fp, fs) < 0.5
    assert abs(fp[-1] - fs[-1]) < 0.5


@pytest.mark.fast
def test_qvar_sum_triangle_on_resampled():
    """|S-P| + |P-c| bounds exploratory variation on circle."""
    part = [i / 32 for i in range(33)]
    pl = piecewise_linear_interpolation(circle_param, part)
    sm = round_corners_c1(pl.interpolant, epsilon=0.02)
    from squarepeg.variation.cubic_corner_smoothing import _resample_polyline

    n = min(len(pl.interpolant), len(sm.smoothed), len(pl.original))
    p = _resample_polyline(pl.interpolant, n)
    s = _resample_polyline(sm.smoothed, n)
    c = _resample_polyline(pl.original, n)
    d_sp = path_difference(s, p)
    d_pc = path_difference(p, c)
    q = 1.5
    assert p_variation(d_sp, q) < 1.0
    assert p_variation(d_pc, q) < 1.0


@pytest.mark.fast
def test_refined_circle_primitives_converge():
    vals = []
    for k in range(3, 7):
        n = 2**k
        pts = [circle_param(i / n) for i in range(n + 1)]
        vals.append(primitive_from_points(pts)[-1])
    assert abs(vals[-1] - vals[-2]) < abs(vals[1] - vals[0])


@pytest.mark.fast
def test_lifted_period_offset():
    from squarepeg.variation.young_integral import lift_periodic_primitive

    base = [0.0, 0.1, 0.2, 0.3]
    lifted = lift_periodic_primitive(base, periods=3)
    assert len(lifted) == len(base) * 3 - 2
    assert lifted[-1] > lifted[0]
