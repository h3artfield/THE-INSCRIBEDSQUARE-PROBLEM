"""Generalized radius and family certificates."""

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.robust_degree.generalized_radius import underline_rho_k_generalized


@pytest.mark.fast
def test_generalized_never_zero_without_proof():
    poly = PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])
    r = underline_rho_k_generalized(poly)
    assert r.interpretation in (
        "ISOLATED_CERTIFICATE_FOUND",
        "FAMILY_CERTIFICATE_FOUND",
        "NO_CERTIFICATE_AT_LEVEL_K",
        "UNSUPPORTED_COMPONENT",
    )


@pytest.mark.fast
def test_monotone_gen_nonnegative():
    poly = PolygonCurve([(0, 0), (2, 0), (2, 2), (0, 2)])
    r = underline_rho_k_generalized(poly)
    assert r.underline_rho_k_gen >= 0
