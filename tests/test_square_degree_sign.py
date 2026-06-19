"""Jacobian sign and degree tests."""

import pytest

from squarepeg.residual_curves.iv_backend_v1 import contains_zero, det_interval_on_box
from squarepeg.residual_curves.square_boundary_degree import certify_boundary_exclusion
from squarepeg.residual_curves.t025_frozen_constants import KRAWCZYK_THETA_BOXES


@pytest.mark.fast
def test_det_excludes_zero_on_box():
    boxes = tuple((float(a), float(b)) for a, b in KRAWCZYK_THETA_BOXES)
    det_iv = det_interval_on_box(boxes)
    assert not contains_zero(det_iv)


@pytest.mark.fast
def test_degree_matches_det_sign():
    cert = certify_boundary_exclusion(max_depth=5)
    assert cert.degree == cert.det_sign
    assert cert.degree != 0
