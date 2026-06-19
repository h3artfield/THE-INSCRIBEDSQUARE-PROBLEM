"""T027 robustness certificate tests."""

import pytest

from squarepeg.residual_curves.c0_square_perturbation import build_c0_certificate
from squarepeg.residual_curves.square_boundary_degree import certify_boundary_exclusion


@pytest.mark.fast
def test_positive_eta0():
    bnd = certify_boundary_exclusion(max_depth=5)
    c0 = build_c0_certificate(bnd.boundary_margin)
    assert c0.eta0 > 0
    assert c0.perturbation_sufficient()
    assert c0.E_eta0 < bnd.boundary_margin


@pytest.mark.fast
def test_nondegeneracy_margin():
    bnd = certify_boundary_exclusion(max_depth=5)
    c0 = build_c0_certificate(bnd.boundary_margin)
    assert c0.d_min > 4 * c0.eta0 or c0.eta0 < c0.d_min / 3
    assert c0.side_length_lower_bound > 0.35
