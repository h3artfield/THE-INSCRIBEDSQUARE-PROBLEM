"""Directive 028 — cluster crosscut and T051."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.cluster_crosscut import (
    apply_cluster_surgery,
    cluster_crosscut,
    prove_cluster_crosscut_exists,
)
from squarepeg.defect_extraction.dirty_examples import example_dirty_saturatable_two_gate


@pytest.mark.fast
def test_crosscut_exists():
    _, cluster, _ = example_dirty_saturatable_two_gate()
    assert prove_cluster_crosscut_exists(cluster)
    cross = cluster_crosscut(cluster)
    assert cross.start == cluster.gate_a


@pytest.mark.fast
def test_cluster_surgery_jordan():
    verts, cluster, _ = example_dirty_saturatable_two_gate()
    res = apply_cluster_surgery(verts, cluster, 1, 3)
    assert res.crosscut is not None
