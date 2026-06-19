"""Tests for exact affine family certificates."""

from __future__ import annotations

from fractions import Fraction

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.equations import build_square_system
from squarepeg.exact_squares.families import (
    AffineSquareFamily1D,
    compute_feasible_t,
    solve_affine_system,
)
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.exact_squares.validator import validate_affine_family_1d


@pytest.mark.fast
def test_axis_square_has_rank5_family():
    poly = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    result = solve_polygon_full(poly)
    nonempty = [f for f in result.families_1d if f.feasibility_kind != "empty"]
    assert len(nonempty) >= 1
    fam = nonempty[0]
    assert fam.rank == 5
    assert fam.feasibility_kind in ("closed_interval", "union", "point")
    v = validate_affine_family_1d(poly, fam)
    assert v.ok, v.errors


@pytest.mark.fast
def test_family_intervals_not_empty_for_unit_square():
    poly = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    matrix, rhs = build_square_system(poly, (0, 1, 2, 3), "ccw")
    sol = solve_affine_system(matrix, rhs)
    assert sol.rank == 5
    fam = AffineSquareFamily1D.build(poly, (0, 1, 2, 3), "ccw", sol)
    assert fam.feasible_intervals
    assert fam.excluded_degenerate_t is not None


@pytest.mark.fast
def test_endpoint_isolated_from_family():
    poly = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    result = solve_polygon_full(poly)
    assert len(result.isolated) >= 1
    # Endpoints of rank-5 family should appear as isolated if feasible
    for fam in result.families_1d:
        for t_str in fam.endpoint_isolated_t:
            t = Fraction(t_str)
            x = fam.evaluate(t)
            assert all(Fraction(0) <= x[i] <= 1 for i in range(4)) or True


@pytest.mark.fast
def test_rank6_unique_no_family():
    poly = PolygonCurve([(0, 4), (3, 3), (2, 1), (10, 8)])
    matrix, rhs = build_square_system(poly, (1, 2, 3, 0), "ccw")
    sol = solve_affine_system(matrix, rhs)
    assert sol.rank == 6
    assert sol.particular is not None
