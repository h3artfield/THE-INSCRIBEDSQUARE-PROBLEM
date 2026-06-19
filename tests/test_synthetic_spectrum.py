"""Synthetic spectrum diagnostic tests."""

import pytest

from squarepeg.spectral_axioms.synthetic_spectrum import run_all_synthetic_tests


@pytest.mark.fast
def test_synthetic_suite_runs():
    results = run_all_synthetic_tests()
    assert len(results) >= 3
    names = {r.test_name for r in results}
    assert "single_branch_a_prime_equals_g_star_derivative" in names


@pytest.mark.fast
def test_positive_radius_fails_at_midpoint():
    results = run_all_synthetic_tests()
    pos = next(r for r in results if r.test_name == "positive_radius_at_midpoint")
    assert pos.can_represent_g_star is False


@pytest.mark.fast
def test_branch_duality_symmetric_compatible():
    results = run_all_synthetic_tests()
    duality = next(r for r in results if r.test_name == "branch_duality_a_prime_symmetric")
    assert duality.can_represent_g_star is True
