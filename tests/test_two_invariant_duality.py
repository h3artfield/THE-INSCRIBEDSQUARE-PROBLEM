"""Two-invariant duality LP tests."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.two_invariant_model import TwoInvariantConfig, solve_two_invariant


@pytest.mark.fast
def test_duality_at_midpoint_kappa_one():
    cfg = TwoInvariantConfig(N=40, kappa=Fraction(1), k=1)
    res = solve_two_invariant(cfg)
    assert res.status == "optimal"
    assert res.optimum_g2_midpoint == Fraction(1)
    # indexed duality: g1(x)+g2(1-x)=1
    N = cfg.N
    for i in range(N + 1):
        assert res.g1_values[i] + res.g2_values[N - i] == Fraction(1)


@pytest.mark.fast
def test_duality_does_not_strengthen_at_eleven_tenths():
    cfg = TwoInvariantConfig(N=40, kappa=Fraction(11, 10), k=1)
    res = solve_two_invariant(cfg)
    assert res.status == "optimal"
    assert res.optimum_g2_midpoint == Fraction(0)
