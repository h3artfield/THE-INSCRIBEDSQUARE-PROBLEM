"""Regression: rationalized regular hexagon — exact solver vs sampled oracle."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from fractions import Fraction

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.exact_squares.validator import validate_geometry

FIXTURE = Path(__file__).resolve().parents[1] / "data" / "regressions" / "rationalized_regular_hexagon.json"


@pytest.fixture
def hexagon() -> PolygonCurve:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return PolygonCurve(data["vertices"])


@pytest.mark.fast
def test_fixture_simple_ccw(hexagon: PolygonCurve):
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["simple"] is True
    assert data["orientation"] == "ccw"
    assert hexagon.signed_area() > 0
    assert hexagon.signed_area() == Fraction(data["signed_area"])


@pytest.mark.fast
def test_exact_solver_finds_squares(hexagon: PolygonCurve):
    result = solve_polygon_full(hexagon, allow_repeated_edges=True)
    assert result.stats["isolated_count"] >= 1
    assert result.stats["unsupported_count"] == 0
    for cert in result.isolated:
        assert cert.certificate_type == "exact"
        ok = validate_geometry(
            hexagon,
            cert.edge_indices,
            tuple(Fraction(p) for p in cert.edge_parameters),
        )
        assert ok.ok


@pytest.mark.fast
def test_oracle_false_negative_documented(hexagon: PolygonCurve):
    """Oracle is sampled only — zero does not imply no square (see F012)."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    exact = solve_polygon_full(hexagon).stats["isolated_count"]
    assert exact >= 1
    assert "false negative" in data["oracle_note"].lower()
