"""Tests for T025 compactness / interval certificate."""

import pytest

from squarepeg.residual_curves.interval_square_solver import compactness_side_lower_bound
from squarepeg.residual_curves.limit_square import (
    build_compactness_certificate,
    verify_truncation_certificates,
)


@pytest.mark.fast
def test_compactness_side_bound():
    assert compactness_side_lower_bound() >= 0.45


@pytest.mark.fast
def test_truncation_exact_certificates():
    certs = verify_truncation_certificates(4)
    assert len(certs) >= 1


@pytest.mark.fast
def test_t025_compactness_certificate():
    cert = build_compactness_certificate(3, 4)
    assert cert.certification_status == "certified"
    assert cert.side_lower_bound_uniform > 0
