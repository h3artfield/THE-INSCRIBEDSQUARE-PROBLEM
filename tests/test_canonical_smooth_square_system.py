"""Tests for smooth square system."""

import math

import pytest

from squarepeg.residual_curves.double_spiral import gamma_plus, r_outer
from squarepeg.residual_curves.smooth_square_system import (
    DISCOVERED_SMOOTH_THETA,
    square_map_F_theta,
)


@pytest.mark.fast
def test_discovered_root_near_zero():
    f = square_map_F_theta(list(DISCOVERED_SMOOTH_THETA))
    assert max(abs(v) for v in f) < 1e-10


@pytest.mark.fast
def test_vertices_on_smooth_outer_arm():
    for th in DISCOVERED_SMOOTH_THETA:
        x, y = gamma_plus(th)
        assert abs(math.hypot(x, y) - r_outer(th)) < 1e-12


@pytest.mark.fast
def test_side_length_positive():
    p0 = gamma_plus(DISCOVERED_SMOOTH_THETA[0])
    p1 = gamma_plus(DISCOVERED_SMOOTH_THETA[1])
    assert math.hypot(p0[0] - p1[0], p0[1] - p1[1]) > 0.4
