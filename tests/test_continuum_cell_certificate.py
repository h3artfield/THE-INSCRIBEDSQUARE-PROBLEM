"""Exact cell subadditivity certificates."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.continuum_cells import PLFunction, certify_pl_subadditivity
from squarepeg.spectral_axioms.grid_model import GridLPConfig, solve_grid_lp


@pytest.mark.fast
def test_linear_g_subadditive_cells():
    N = 10
    values = [Fraction(i, N) for i in range(N + 1)]
    pl = PLFunction.from_grid(values, N)
    cert = certify_pl_subadditivity(pl)
    assert cert.ok
    assert cert.min_H == 0
    assert len(cert.cells) > 0


@pytest.mark.fast
def test_n40_witness_subadditive_continuum():
    N = 40
    r = solve_grid_lp(GridLPConfig(N=N, kappa=Fraction(11, 10), k=1))
    pl = PLFunction.from_grid(r.values, N)
    cert = certify_pl_subadditivity(pl)
    assert cert.ok, cert.violations[:3]
    assert cert.min_H >= 0


@pytest.mark.fast
def test_n160_witness_fails_subadditivity():
    N = 160
    r = solve_grid_lp(GridLPConfig(N=N, kappa=Fraction(11, 10), k=1))
    pl = PLFunction.from_grid(r.values, N)
    cert = certify_pl_subadditivity(pl)
    assert not cert.ok
    assert cert.min_H < 0
