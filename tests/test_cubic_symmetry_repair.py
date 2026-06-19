"""Regression: cubic midpoint value vs derivative (Directive 005)."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.cubic_countermodel import (
    g_star,
    g_star_derivative,
    g_star_derivative_factored,
)


@pytest.mark.fast
def test_g_star_at_half_is_one_half():
    """Collapse signature is g_*'(1/2)=0, NOT g_*(1/2)=0."""
    assert g_star(Fraction(1, 2)) == Fraction(1, 2)
    assert g_star(Fraction(1, 2)) != 0


@pytest.mark.fast
def test_g_star_derivative_zero_at_half():
    assert g_star_derivative(Fraction(1, 2)) == 0
    assert g_star_derivative_factored(Fraction(1, 2)) == 0


@pytest.mark.fast
def test_derivative_symmetry_reflection():
    """g_*'(1-x) = g_*'(x) for all x."""
    for i in range(21):
        x = Fraction(i, 20)
        assert g_star_derivative(1 - x) == g_star_derivative(x)


@pytest.mark.fast
def test_action_symmetry_g_one_minus_x():
    from squarepeg.spectral_axioms.cubic_countermodel import g_star_dual

    for i in range(21):
        x = Fraction(i, 20)
        assert g_star_dual(x) == 1 - g_star(x)
