"""Tests for chord-curve homotopy endpoints."""

import pytest

from squarepeg.residual_curves.chord_curve_homotopy import F_lambda, homotopy_point
from squarepeg.residual_curves.smooth_square_system import supports_from_theta_windows


@pytest.mark.fast
def test_homotopy_at_lambda_one_is_smooth():
    sup = supports_from_theta_windows()
    a, b = (0.3, 0.0), (0.2, 0.1)
    p = homotopy_point(1.0, 0.5, a, b, sup[0])
    assert abs(p[0]) < 1.0
