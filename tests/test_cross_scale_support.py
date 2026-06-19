"""Cross-scale support pattern tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_geometry.cross_scale_rhombus import search_cross_scale_support


@pytest.mark.fast
def test_geometric_candidate_k1():
    r = search_cross_scale_support()
    assert len(r.candidates) >= 1
    assert r.geometric_fixed_scale
    assert not r.certified_cyclic_odd


@pytest.mark.fast
def test_deep_level_side_collapses():
    r = search_cross_scale_support()
    k_deep = r.candidates[-1]
    k1 = r.candidates[0]
    assert k_deep.side_estimate < k1.side_estimate
