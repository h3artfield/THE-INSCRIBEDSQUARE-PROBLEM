"""Tests for T025 uniform lower bounds and smooth-curve gap."""

import math
from fractions import Fraction

import pytest

from squarepeg.residual_curves.truncation_audit import (
    literal_side_length_squared,
    macro_square_certificate,
    min_vertex_radius_lower_bound,
    vertex_on_smooth_outer_arm,
)


@pytest.mark.fast
def test_rational_side_length_positive():
    s2 = literal_side_length_squared()
    assert s2 > 0


@pytest.mark.fast
def test_min_vertex_radius_bound():
    assert min_vertex_radius_lower_bound() >= Fraction(11, 50)


@pytest.mark.fast
def test_vertices_not_on_smooth_outer_arm():
    """Audit gap: polygon square vertices lie on chords, not on gamma_+."""
    cert = macro_square_certificate(5)
    assert cert is not None
    for v in cert.vertices:
        assert not vertex_on_smooth_outer_arm(v, tol=1e-3)


@pytest.mark.fast
def test_side_length_rational_positive():
    side = math.sqrt(float(literal_side_length_squared()))
    assert side > 0.08
