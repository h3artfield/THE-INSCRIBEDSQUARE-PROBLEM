"""Independent validation and SymPy differential testing."""

from __future__ import annotations

import random

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.equations import build_square_system
from squarepeg.exact_squares.families import solve_affine_system
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.exact_squares.sympy_checker import compare_systems, save_fixture
from squarepeg.exact_squares.validator import (
    validate_affine_family_1d,
    validate_geometry,
    validate_square_certificate,
)

pytest.importorskip("sympy")


@pytest.mark.fast
def test_all_isolated_pass_independent_validator():
    poly = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    result = solve_polygon_full(poly)
    for cert in result.isolated:
        v = validate_square_certificate(poly, cert)
        assert v.ok, v.errors


@pytest.mark.fast
def test_validator_reconstructs_vertices():
    poly = PolygonCurve([(0, 4), (3, 3), (2, 1), (10, 8)])
    result = solve_polygon_full(poly)
    assert result.isolated
    cert = result.isolated[0]
    from fractions import Fraction
    from squarepeg.exact_squares.validator import reconstruct_vertices

    params = tuple(Fraction(p) for p in cert.edge_parameters)
    rebuilt = reconstruct_vertices(poly, cert.edge_indices, params)
    stored = tuple((Fraction(a), Fraction(b)) for a, b in cert.vertices)
    assert rebuilt == stored


@pytest.mark.fast
def test_sympy_agrees_on_corpus():
    rng = random.Random(0)
    polys = [
        PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)]),
        PolygonCurve([(0, 4), (3, 3), (2, 1), (10, 8)]),
    ]
    for poly in polys:
        n = poly.num_edges
        for _ in range(5):
            edges = tuple(rng.randint(0, n - 1) for _ in range(4))
            for rot in ("ccw", "cw"):
                cmp = compare_systems(poly, edges, rot)
                if not cmp["match"]:
                    save_fixture(cmp, f"mismatch_{poly.polygon_hash()[:8]}_{edges}_{rot}")
                assert cmp["match"], cmp


@pytest.mark.fast
def test_families_pass_independent_validation():
    poly = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    result = solve_polygon_full(poly)
    for fam in result.families_1d:
        v = validate_affine_family_1d(poly, fam)
        assert v.ok, v.errors
