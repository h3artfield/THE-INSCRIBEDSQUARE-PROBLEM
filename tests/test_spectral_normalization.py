"""Tests for spectral normalization."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.normalization import (
    B_from_area_radius,
    kappa_from_B,
    midpoint_quotient,
    normalize_spectral,
)


@pytest.mark.fast
def test_B_kappa_circle_extremum():
    B = B_from_area_radius(1, 1 / 2)  # area 1, diameter 1
    assert B == Fraction(4)
    k = kappa_from_B(B)
    assert k > 0


@pytest.mark.fast
def test_normalize_endpoints():
    assert normalize_spectral(0, 10) == 0
    assert normalize_spectral(10, 10) == 1


@pytest.mark.fast
def test_midpoint_quotient_linear():
    # g(x)=x => D_h = 1
    q = midpoint_quotient(Fraction(1, 2) - Fraction(1, 10), Fraction(1, 2) + Fraction(1, 10), Fraction(1, 10))
    assert q == Fraction(1)
