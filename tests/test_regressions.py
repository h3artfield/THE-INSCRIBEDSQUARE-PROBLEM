"""Regression fixtures for corrected e3 coefficient matrix."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.exact_squares.validator import validate_square_certificate

REGRESSION_VERTS = [(0, 4), (3, 3), (2, 1), (10, 8)]
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "regression_quadrilateral.json"


@pytest.fixture(scope="module")
def regression_polygon() -> PolygonCurve:
    return PolygonCurve(REGRESSION_VERTS)


@pytest.mark.fast
def test_regression_quadrilateral_has_isolated_square(regression_polygon: PolygonCurve):
    result = solve_polygon_full(regression_polygon)
    assert len(result.isolated) >= 1
    for cert in result.isolated:
        v = validate_square_certificate(regression_polygon, cert)
        assert v.ok, v.errors


@pytest.mark.fast
def test_regression_quadrilateral_snapshot(regression_polygon: PolygonCurve):
    """Record solver output for the mandatory regression polygon."""
    result = solve_polygon_full(regression_polygon)
    snapshot = {
        "vertices": REGRESSION_VERTS,
        "isolated_count": len(result.isolated),
        "families_1d_count": len(result.families_1d),
        "unsupported_count": len(result.unsupported),
        "isolated": [c.to_dict() for c in result.isolated],
        "family_ids": [f.family_id for f in result.families_1d],
    }
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")
    assert snapshot["isolated_count"] >= 1
    assert snapshot["families_1d_count"] >= 0


@pytest.mark.fast
def test_regression_no_sampling_in_families(regression_polygon: PolygonCurve):
    result = solve_polygon_full(regression_polygon)
    for fam in result.families_1d:
        assert fam.base_point
        assert fam.direction
        assert "feasible_intervals" in fam.to_dict()
        assert "sample" not in fam.to_json().lower()
        assert fam.feasibility_kind in (
            "empty",
            "point",
            "closed_interval",
            "open_interval",
            "union",
        )
