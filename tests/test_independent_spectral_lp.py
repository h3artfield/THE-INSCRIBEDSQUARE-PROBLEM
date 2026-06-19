"""Independent LP replication tests."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.grid_model import GridLPConfig, solve_grid_lp
from squarepeg.spectral_axioms.independent_lp import compare_with_primary, solve_independent


@pytest.mark.fast
def test_independent_matches_primary_kappa_one():
    cfg = GridLPConfig(N=40, kappa=Fraction(1), k=1)
    primary = solve_grid_lp(cfg)
    ind = solve_independent(40, Fraction(1), 1)
    assert ind["success"]
    assert ind["optimum"] == primary.optimum


@pytest.mark.fast
def test_independent_matches_primary_kappa_eleven_tenths():
    cfg = GridLPConfig(N=40, kappa=Fraction(11, 10), k=1)
    primary = solve_grid_lp(cfg)
    cmp = compare_with_primary(primary.values, primary.optimum, 40, Fraction(11, 10))
    assert cmp["match_optimum"]


@pytest.mark.fast
def test_independent_matches_primary_kappa_101_100():
    cfg = GridLPConfig(N=80, kappa=Fraction(101, 100), k=1)
    primary = solve_grid_lp(cfg)
    cmp = compare_with_primary(primary.values, primary.optimum, 80, Fraction(101, 100))
    assert cmp["match_optimum"]
