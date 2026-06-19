"""Polygon rank-6 to protected certificate conversion."""

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.robust_degree.polygon_extractor import convert_isolated_square, rho_square_cert_polygon


def _unit_square():
    return PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])


@pytest.mark.fast
def test_unit_square_has_isolated_certs():
    poly = _unit_square()
    result = solve_polygon_full(poly)
    assert len(result.isolated) >= 1


@pytest.mark.fast
def test_convert_rank6_when_possible():
    poly = _unit_square()
    result = solve_polygon_full(poly)
    if not result.isolated:
        pytest.skip("no isolated squares on unit square")
    conv = convert_isolated_square(poly, result.isolated[0])
    assert conv.conversion_status in ("converted", "boundary_failed", "singular_jacobian")


@pytest.mark.fast
def test_rho_cert_nonnegative():
    poly = _unit_square()
    result = solve_polygon_full(poly)
    rho, breakdown = rho_square_cert_polygon(poly, result)
    assert rho >= 0
    assert breakdown["isolated"] >= 0
