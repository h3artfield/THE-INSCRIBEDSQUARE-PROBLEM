"""Tests for cubic countermodel g_*."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.cubic_countermodel import (
    D_h,
    H_factored,
    H_subadditivity,
    g_star,
    g_star_at_half_minus_h,
    g_star_at_half_plus_h,
    g_star_centered,
    g_star_derivative,
    g_star_derivative_factored,
    g_star_dual,
    strict_increase_proof_values,
    verify_all_identities,
)


@pytest.mark.fast
def test_endpoints():
    assert g_star(0) == 0
    assert g_star(1) == 1


@pytest.mark.fast
def test_centered_form():
    for i in range(21):
        x = Fraction(i, 20)
        assert g_star(x) == g_star_centered(x)


@pytest.mark.fast
def test_derivative_factorization():
    for i in range(21):
        x = Fraction(i, 20)
        assert g_star_derivative(x) == g_star_derivative_factored(x)


@pytest.mark.fast
def test_lipschitz_constant_three():
    facts = verify_all_identities()
    assert facts.lip_constant == 3
    assert facts.max_derivative == 3
    assert g_star_derivative(0) == 3
    assert g_star_derivative(1) == 3
    assert g_star(Fraction(1, 2)) == Fraction(1, 2)
    assert g_star_derivative(Fraction(1, 2)) == 0


@pytest.mark.fast
def test_subadditivity_factorization():
    for i in range(11):
        for j in range(11):
            x, y = Fraction(i, 10), Fraction(j, 10)
            if x + y <= 1:
                assert H_subadditivity(x, y) == H_factored(x, y)
                assert H_subadditivity(x, y) >= 0


@pytest.mark.fast
def test_symmetry_duality():
    for i in range(21):
        x = Fraction(i, 20)
        assert g_star_dual(x) == 1 - g_star(x)


@pytest.mark.fast
def test_midpoint_D_h():
    for k in range(1, 15):
        h = Fraction(k, 30)
        assert g_star(Fraction(1, 2) + h) == g_star_at_half_plus_h(h)
        assert g_star(Fraction(1, 2) - h) == g_star_at_half_minus_h(h)
        assert D_h(Fraction(1, 2), h) == 4 * h**2


@pytest.mark.fast
def test_strict_increase_integral():
    assert strict_increase_proof_values(Fraction(0), Fraction(1, 2)) > 0
    assert strict_increase_proof_values(Fraction(1, 2), Fraction(1)) > 0
    assert strict_increase_proof_values(Fraction(1, 4), Fraction(3, 4)) > 0


@pytest.mark.fast
def test_verify_all_identities():
    facts = verify_all_identities()
    assert facts.endpoints_ok
    assert facts.centered_form_ok
    assert facts.derivative_factorization_ok
    assert facts.subadditivity_factorization_ok
    assert facts.symmetry_ok
    assert facts.D_h_formula_ok
