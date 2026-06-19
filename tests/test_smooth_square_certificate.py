"""Tests for smooth square certificate."""

import pytest

from squarepeg.residual_curves.smooth_square_certificate import (
    certify_discovered_root,
    validate_certificate_independent,
)


@pytest.mark.fast
def test_direct_interval_certificate():
    cert = certify_discovered_root(radius=0.15)
    assert cert.certification_status == "certified"
    assert cert.side_length_lower_bound >= 0.42
    assert cert.min_radius_lower_bound >= 0.24
    assert validate_certificate_independent(cert)
