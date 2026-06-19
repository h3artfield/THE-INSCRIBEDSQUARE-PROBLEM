"""Tests for grid LP constraints."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.exact_verify import verify_grid_solution, verify_midpoint_objective
from squarepeg.spectral_axioms.grid_model import GridLPConfig, solve_grid_lp


@pytest.mark.fast
def test_linear_witness_satisfies_level_f():
    N = 20
    values = [Fraction(i, N) for i in range(N + 1)]
    cfg = GridLPConfig(N=N, kappa=Fraction(10), k=1)
    ok, errs = verify_grid_solution(values, cfg)
    assert ok, errs


@pytest.mark.fast
def test_kappa_one_forces_midpoint_one():
    cfg = GridLPConfig(N=40, kappa=Fraction(1), k=1)
    res = solve_grid_lp(cfg)
    assert res.status == "optimal"
    obj = verify_midpoint_objective(res.values, cfg)
    assert obj == Fraction(1)
    ok, errs = verify_grid_solution(res.values, cfg)
    assert ok, errs


@pytest.mark.fast
def test_kappa_eleven_tenths_countermodel():
    cfg = GridLPConfig(N=40, kappa=Fraction(11, 10), k=1)
    res = solve_grid_lp(cfg)
    assert res.status == "optimal"
    obj = verify_midpoint_objective(res.values, cfg)
    assert obj == Fraction(0)
    ok, errs = verify_grid_solution(res.values, cfg)
    assert ok, errs
