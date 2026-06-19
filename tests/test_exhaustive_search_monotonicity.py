"""Exhaustive search monotonicity and result codes."""

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.robust_degree.exhaustive_polygon_search import exhaustive_polygon_search


@pytest.mark.fast
def test_never_claims_intrinsic_zero():
    poly = PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])
    report = exhaustive_polygon_search(poly)
    assert report.never_claims_intrinsic_zero
    assert report.final_result in (
        "CERTIFIED_POSITIVE",
        "NOT_FOUND_AT_LEVEL_K",
        "UNSUPPORTED_DEGREE_CASE",
        "NO_PROTECTED_BOX_AT_LEVEL",
    )


@pytest.mark.fast
def test_underline_rho_infty_monotone_levels():
    poly = PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])
    report = exhaustive_polygon_search(poly)
    rhos = [lev.underline_rho_k for lev in report.levels]
    for i in range(len(rhos) - 1):
        assert rhos[i] <= rhos[i + 1] + 1e-12 or rhos[i + 1] == 0.0
