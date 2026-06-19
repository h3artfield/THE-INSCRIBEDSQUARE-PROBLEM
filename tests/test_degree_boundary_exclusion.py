"""Tests for degree boundary exclusion."""

import pytest

from squarepeg.residual_curves.smooth_square_system import OUTER_THETA_WINDOWS
from squarepeg.residual_curves.square_degree import initial_degree_nonsingular


@pytest.mark.fast
def test_jacobian_det_nonzero_at_root():
    from squarepeg.residual_curves.smooth_square_system import DISCOVERED_SMOOTH_THETA

    det = initial_degree_nonsingular(list(DISCOVERED_SMOOTH_THETA))
    assert abs(det) > 1e-6
