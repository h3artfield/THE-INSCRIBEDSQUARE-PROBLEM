"""C^0 error bound verification."""

import pytest

from squarepeg.residual_curves.c0_square_perturbation import (
    F_perturbation_bound,
    R_max_on_support_boxes,
    squared_distance_perturbation_bound,
)


@pytest.mark.fast
def test_squared_distance_bound_independent():
    R = 0.5
    eta = 0.01
    # Worst case: a=(R,0), b=(-R,0), a'=(R+eta,0), b'=(-R-eta,0)
    a, b = (R, 0.0), (-R, 0.0)
    ap, bp = (R + eta, 0.0), (-R - eta, 0.0)
    lhs = abs((ap[0] - bp[0]) ** 2 - (a[0] - b[0]) ** 2)
    rhs = squared_distance_perturbation_bound(eta, R)
    assert lhs <= rhs + 1e-12


@pytest.mark.fast
def test_F_bound_scales_with_eta():
    eta = 0.001
    assert F_perturbation_bound(eta) < F_perturbation_bound(2 * eta)
    assert R_max_on_support_boxes() > 0.2
