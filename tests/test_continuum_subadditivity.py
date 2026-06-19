"""Continuum subadditivity verification — cell certification preferred."""

from __future__ import annotations

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.continuum_cells import PLFunction, certify_pl_subadditivity
from squarepeg.spectral_axioms.grid_model import GridLPConfig, solve_grid_lp


@pytest.mark.fast
def test_n40_model_w_countermodel_cell_certified():
    """Model W countermodel at kappa=11/10: flat at midpoint, subadditive on T."""
    N = 40
    r = solve_grid_lp(GridLPConfig(N=N, kappa=Fraction(11, 10), k=1))
    pl = PLFunction.from_grid(r.values, N)
    cert = certify_pl_subadditivity(pl)
    assert cert.ok
    half = Fraction(1, 2)
    h = Fraction(1, N)
    d_h = (pl.value_at(half + h) - pl.value_at(half - h)) / (2 * h)
    assert d_h == 0
