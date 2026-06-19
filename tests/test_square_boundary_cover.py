"""Boundary exclusion cover tests."""

import pytest

from squarepeg.residual_curves.square_boundary_degree import (
    certify_boundary_exclusion,
    validate_boundary_certificate,
)


@pytest.mark.fast
def test_boundary_cover_and_margin():
    cert = certify_boundary_exclusion(max_depth=6)
    assert cert.boundary_margin > 0
    assert cert.det_sign in (-1, 1)
    assert cert.degree != 0
    assert len(cert.terminal_cells) > 0
    assert validate_boundary_certificate(cert)


@pytest.mark.fast
def test_global_margin_recomputed():
    cert = certify_boundary_exclusion(max_depth=5)
    m = min(c.margin for c in cert.terminal_cells)
    assert m >= cert.boundary_margin * 0.99
