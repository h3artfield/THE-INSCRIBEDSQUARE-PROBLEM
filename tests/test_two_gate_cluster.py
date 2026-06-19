"""Directive 028 — two-gate cluster tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.dirty_examples import example_dirty_saturatable_two_gate


@pytest.mark.fast
def test_dirty_lobe_saturatable_two_gate():
    verts, cluster, ok = example_dirty_saturatable_two_gate()
    assert len(verts) >= 5
    assert cluster.hull.is_jordan_disk
    assert ok
