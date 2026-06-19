"""Tests for truncation uniform convergence."""

import math

import pytest

from squarepeg.residual_curves.canonical import CANONICAL_THETA0, CanonicalDoubleSpiral
from squarepeg.residual_curves.truncation_audit import (
    describe_edge,
    hausdorff_to_outer_arm,
    vertex_count,
)


@pytest.mark.fast
def test_vertex_count_formula():
    assert vertex_count(3) == 17
    assert vertex_count(7) == 33


@pytest.mark.fast
def test_outer_arm_edges_not_artificial():
    for e in (0, 3, 5):
        d = describe_edge(5, e)
        assert d.kind == "outer_arm"
        assert not d.is_artificial


@pytest.mark.fast
def test_outer_connector_index():
    d = describe_edge(5, 4 * 5 + 3)
    assert d.kind == "outer_connector"
    assert not d.is_artificial


@pytest.mark.fast
def test_hausdorff_outer_arm_decreases():
    d3 = hausdorff_to_outer_arm(3)
    d7 = hausdorff_to_outer_arm(7)
    assert d7 <= d3 + 1e-9


@pytest.mark.fast
def test_edge_4n_plus_1_is_inner_arm():
    """Directive 011 misreported (4N+1); it is inner-arm segment, not connector."""
    for n in (3, 5, 7):
        d = describe_edge(n, 4 * n + 1)
        assert d.kind == "inner_arm"
