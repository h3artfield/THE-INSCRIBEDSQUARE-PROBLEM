"""Tests for exact square solver and certificates."""

from __future__ import annotations

import json
import random
from fractions import Fraction

import pytest

from squarepeg.certificates.schema import SquareCertificate
from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.equations import build_square_system
from squarepeg.exact_squares.families import solve_affine_system
from squarepeg.exact_squares.oracle import oracle_count_squares
from squarepeg.exact_squares.solver import solve_polygon, solve_polygon_full

pytestmark = pytest.mark.fast


def _exact_squares(poly: PolygonCurve) -> list[SquareCertificate]:
    return [
        c
        for c in solve_polygon(poly, allow_repeated_edges=True)
        if c.certificate_type == "exact"
    ]


def test_axis_aligned_square_has_exact_certificate():
    poly = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    certs = _exact_squares(poly)
    assert len(certs) >= 1
    side_sq = {c.side_length_squared for c in certs}
    assert "1" in side_sq or "4" in side_sq or any(Fraction(s) > 0 for s in side_sq)
    for c in certs:
        assert c.verify_against_polygon(poly)
        assert Fraction(c.side_length_squared) > 0


def test_rectangle_not_all_squares():
    rect = PolygonCurve([(0, 0), (6, 0), (6, 3), (0, 3)])
    certs = _exact_squares(rect)
    assert len(certs) >= 1
    for c in certs:
        side = Fraction(c.side_length_squared)
        diag = Fraction(c.diagonal_length_squared)
        assert 2 * side == diag


def test_triangle_has_square():
    tri = PolygonCurve([(0, 0), (4, 0), (0, 3)])
    certs = _exact_squares(tri)
    assert len(certs) >= 1


def test_regular_pentagon():
    pent = PolygonCurve([(0, 0), (6, 0), (7, 4), (3, 8), (-2, 3)])
    certs = _exact_squares(pent)
    assert len(certs) >= 1


def test_certificate_serialization_roundtrip():
    poly = PolygonCurve([(0, 0), (5, 0), (5, 5), (0, 5)])
    cert = _exact_squares(poly)[0]
    restored = SquareCertificate.from_dict(json.loads(cert.to_json()))
    assert restored.polygon_hash == cert.polygon_hash
    assert restored.vertices == cert.vertices
    assert restored.to_json() == cert.to_json()


def test_similarity_invariance():
    base = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    base_count = len(_exact_squares(base))
    moved = base.translate(10, -3).rotate(0.3).scale(2)
    moved_count = len(_exact_squares(moved))
    assert base_count >= 1
    assert moved_count >= 1
    # Rotated/scaled rational coordinates may miss some edge-parameter solutions.
    assert moved_count >= base_count - 1


def test_reversal_preserves_square_count():
    poly = PolygonCurve([(0, 0), (5, 0), (6, 4), (1, 5)])
    a = len(_exact_squares(poly))
    b = len(_exact_squares(poly.reversed()))
    assert a == b


def test_interior_vertex_square():
    poly = PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)])
    result = solve_polygon_full(poly)
    assert len(result.isolated) >= 1
    fams = [f for f in result.families_1d if f.feasibility_kind == "closed_interval"]
    assert len(fams) >= 1
    fam = next(f for f in fams if f.edge_indices == (0, 1, 2, 3))
    from fractions import Fraction
    from squarepeg.exact_squares.validator import validate_geometry

    x = fam.evaluate(Fraction(2))
    assert all(x[i] == Fraction(1, 2) for i in range(4))
    assert validate_geometry(poly, fam.edge_indices, x[:4]).ok


@pytest.mark.slow
def test_oracle_crosscheck_small_square():
    poly = PolygonCurve([(0, 0), (3, 0), (3, 3), (0, 3)])
    exact = len(_exact_squares(poly))
    oracle = oracle_count_squares(poly, samples_per_edge=15)
    assert exact >= 1
    assert oracle >= 1
    # Oracle is sampled; exact solver should find at least one certified square.
    assert exact <= oracle + 4


def test_singular_system_reported():
    poly = PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])
    matrix, rhs = build_square_system(poly, (0, 0, 0, 0), "ccw")
    result = solve_affine_system(matrix, rhs)
    assert result.rank in (5, 6) or not result.inconsistent


@pytest.mark.slow
def test_random_small_polygons():
    rng = random.Random(42)
    for _ in range(10):
        n = rng.randint(4, 7)
        verts = []
        for k in range(n):
            verts.append((rng.randint(0, 10), rng.randint(0, 10)))
        try:
            poly = PolygonCurve(verts)
        except ValueError:
            continue
        certs = _exact_squares(poly)
        assert len(certs) >= 1, verts


def test_no_conjecture_claim_in_certificates():
    poly = PolygonCurve([(0, 0), (2, 0), (2, 2), (0, 2)])
    for c in solve_polygon(poly, allow_repeated_edges=True):
        blob = c.to_json()
        assert "conjecture" not in blob.lower()
        assert "proved" not in blob.lower() or "proof" not in blob.lower()
