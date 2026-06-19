"""Tests for velocity-matched cubic corner smoothing (T018)."""

import math

import pytest

from squarepeg.variation.cubic_corner_smoothing import (
    cubic_bezier_derivative_ds,
    cubic_bezier_eval,
    cubic_control_points,
    cubic_endpoint_velocity_a,
    cubic_endpoint_velocity_c,
    polygon_corner_sample,
    projection_witness,
    remove_collinear_vertices,
    round_corners_c1_cubic,
    w_dot_derivative_positive,
)
from squarepeg.variation.p_variation import euclidean, path_difference, p_variation, total_variation


def _square():
    return [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]


@pytest.mark.fast
def test_cubic_endpoint_positions():
    a, v, c = (0.0, 0.0), (1.0, 1.0), (2.0, 0.0)
    d = 0.3
    q0, q1, q2, q3 = cubic_control_points(a, v, c, d)
    assert euclidean(cubic_bezier_eval(q0, q1, q2, q3, 0.0), a) < 1e-12
    assert euclidean(cubic_bezier_eval(q0, q1, q2, q3, 1.0), c) < 1e-12


@pytest.mark.fast
def test_cubic_endpoint_velocity_match():
    a, v, c = (0.0, 0.0), (1.0, 1.0), (2.0, 0.0)
    d = 0.25
    L = 2 * d
    q0, q1, q2, q3 = cubic_control_points(a, v, c, d)
    u_minus = cubic_endpoint_velocity_a(a, v, d)
    u_plus = cubic_endpoint_velocity_c(v, c, d)
    d0 = cubic_bezier_derivative_ds(q0, q1, q2, q3, 0.0)
    d1 = cubic_bezier_derivative_ds(q0, q1, q2, q3, 1.0)
    assert abs(d0[0] / L - u_minus[0]) < 1e-9
    assert abs(d0[1] / L - u_minus[1]) < 1e-9
    assert abs(d1[0] / L - u_plus[0]) < 1e-9
    assert abs(d1[1] / L - u_plus[1]) < 1e-9


@pytest.mark.fast
def test_w_dot_derivative_positive_convex():
    a, v, c = (0.0, 0.0), (1.0, 1.0), (2.0, 0.0)
    d = 0.2
    L = 2 * d
    q0, q1, q2, q3 = cubic_control_points(a, v, c, d)
    w = projection_witness(a, v, c)
    assert w_dot_derivative_positive(q0, q1, q2, q3, w, L)


@pytest.mark.fast
def test_w_dot_derivative_positive_reflex():
    a, v, c = (0.0, 0.0), (1.0, -0.5), (2.0, 0.0)
    d = 0.15
    L = 2 * d
    q0, q1, q2, q3 = cubic_control_points(a, v, c, d)
    w = projection_witness(a, v, c)
    assert w_dot_derivative_positive(q0, q1, q2, q3, w, L)


@pytest.mark.fast
def test_remove_collinear_and_antiparallel():
    pts = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (2.0, 1.0)]
    out = remove_collinear_vertices(pts)
    assert len(out) == 3


@pytest.mark.fast
def test_common_parametrization_equal_length():
    sp = round_corners_c1_cubic(_square(), epsilon=0.05)
    assert len(sp.polygon) == len(sp.smoothed)


@pytest.mark.fast
def test_variation_error_decay():
    e1 = round_corners_c1_cubic(_square(), epsilon=0.2)
    e2 = round_corners_c1_cubic(_square(), epsilon=0.02)
    d1 = path_difference(e1.polygon, e1.smoothed)
    d2 = path_difference(e2.polygon, e2.smoothed)
    assert total_variation(d2) <= total_variation(d1) + 1e-6


@pytest.mark.fast
def test_q_var_le_one_var_on_difference():
    sp = round_corners_c1_cubic(_square(), epsilon=0.05)
    diff = path_difference(sp.polygon, sp.smoothed)
    for q in (1.0, 1.5, 2.0):
        assert p_variation(diff, q) <= total_variation(diff) + 1e-9


@pytest.mark.fast
def test_orientation_preserved():
    from squarepeg.variation.cubic_corner_smoothing import signed_area

    sp = round_corners_c1_cubic(_square(), epsilon=0.1)
    assert signed_area(sp.smoothed) > 0
