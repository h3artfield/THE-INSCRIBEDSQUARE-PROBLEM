"""Witness strictness and D+ analysis."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.grid_model import GridLPConfig, solve_grid_lp
from squarepeg.spectral_axioms.witness_inspector import inspect_grid_witness


@pytest.mark.fast
def test_n40_witness_not_strict():
    N = 40
    r = solve_grid_lp(GridLPConfig(N=N, kappa=Fraction(11, 10), k=1))
    w = inspect_grid_witness(r.values, N, Fraction(11, 10))
    assert not w.is_strictly_increasing
    assert not w.is_strict_bijection_with_D_plus_zero
    assert len(w.flat_intervals) > 0


@pytest.mark.fast
def test_n40_D_h_zero_at_grid_scale():
    from squarepeg.spectral_axioms.continuum_cells import PLFunction

    N = 40
    r = solve_grid_lp(GridLPConfig(N=N, kappa=Fraction(11, 10), k=1))
    pl = PLFunction.from_grid(r.values, N)
    h = Fraction(1, N)
    half = Fraction(1, 2)
    d_h = (pl.value_at(half + h) - pl.value_at(half - h)) / (2 * h)
    assert d_h == 0


@pytest.mark.fast
def test_model_s_forces_positive_objective():
    cfg = GridLPConfig(N=40, kappa=Fraction(11, 10), k=1, delta=Fraction(1, 1000))
    r = solve_grid_lp(cfg)
    assert r.optimum > 0
