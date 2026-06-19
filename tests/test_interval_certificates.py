"""Interval certificate tests."""

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.intervals import IntervalSquareCertificate, certify_interval_polygon


@pytest.mark.fast
def test_float_polygon_unresolved_not_exact():
    poly = PolygonCurve([(0.1, 0.2), (1.5, 0.0), (1.4, 1.1), (0.0, 0.9)])
    cert = certify_interval_polygon(poly)
    assert isinstance(cert, IntervalSquareCertificate)
    assert cert.certification_status == "unresolved"
    assert cert.side_length_lower_bound is None


@pytest.mark.fast
def test_interval_no_exact_promotion():
    cert = certify_interval_polygon(PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)]))
    assert "approximate" in cert.message.lower() or "unresolved" in cert.message.lower()
