"""Variation norm monotonicity: |h|_{q-var} <= |h|_{1-var} for q >= 1."""

import pytest

from squarepeg.variation.p_variation import p_variation, q_variation_bounded_by_total, total_variation


@pytest.mark.fast
def test_two_jump_path():
    pts = [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0)]
    for q in (1.0, 1.25, 1.5, 2.0, 3.0):
        assert q_variation_bounded_by_total(pts, q)


@pytest.mark.fast
def test_zigzag():
    pts = [(0.0, 0.0), (0.25, 0.1), (0.5, 0.0), (0.75, 0.1), (1.0, 0.0)]
    for q in (1.5, 2.0):
        assert p_variation(pts, q) <= total_variation(pts) + 1e-9


@pytest.mark.fast
def test_partition_inequality_direct():
    """(sum |Δ|^q)^{1/q} <= sum |Δ| for single partition."""
    deltas = [0.3, 0.5, 0.2]
    for q in (1.5, 2.0):
        lhs = sum(d**q for d in deltas) ** (1 / q)
        rhs = sum(deltas)
        assert lhs <= rhs + 1e-12
