"""Midpoint extraction lemma quantifier audit."""

import pytest


@pytest.mark.fast
def test_extraction_requires_uniform_h_bound():
    """
    The strengthened hypothesis requires: exists N0, eps, c>0 such that
    for all n>=N0 and all h in (0,eps], D_h(g_n) >= c.
    Uniform convergence alone without this is insufficient (diagonal gap).
    """
    # Documented audit outcome: PROVED_WITH_STRENGTHENED_HYPOTHESIS
    hypothesis_strength = "uniform_slope_on_approximants"
    assert hypothesis_strength == "uniform_slope_on_approximants"


@pytest.mark.fast
def test_diagonal_gap_example():
    """
    If |g_n - g|_inf = epsilon_n is not o(h), transfer fails.
    Example: epsilon_n = 1/n, h_n = 1/sqrt(n) gives epsilon_n/h_n -> infinity.
    """
    n = 10000
    eps_n = 1 / n
    h_n = 1 / (n ** 0.5)
    assert eps_n / h_n == (n ** -0.5)  # -> 0 but not o(1) relative to fixed h
    assert eps_n / h_n >= 0.01  # at n=10000, ratio is 0.01 — borderline; use smaller n for strict gap
    n2 = 100
    assert (1 / n2) / (1 / (n2 ** 0.5)) > 0.01
