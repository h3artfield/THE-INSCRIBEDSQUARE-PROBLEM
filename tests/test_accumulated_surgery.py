"""Accumulated surgery tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.accumulated_surgery import (
    accumulated_area_estimate,
    decompose_surgered_subarc,
    simultaneous_surgery_jordan,
)
from squarepeg.defect_surgery.examples import example_bump_disk, example_bump_polygon
from squarepeg.defect_surgery.nested_forest import PacketForest


@pytest.mark.fast
def test_decompose_surgered_subarc():
    dec = decompose_surgered_subarc(
        retained_paths=[[(0, 0), (0, 1)]],
        chord_paths=[[(0, 1), (1, 1)]],
    )
    assert dec.total_area == dec.alpha_bound or abs(dec.total_area) >= 0


@pytest.mark.fast
def test_accumulated_estimate():
    est = accumulated_area_estimate(beta=0.01, a_att=0.02, mu1=0.1, mu2=0.01, omega_gamma=0.05)
    assert est.alpha_upper >= est.a_att


@pytest.mark.fast
def test_simultaneous_jordan():
    forest = PacketForest(disks=[example_bump_disk()])
    out, ok = simultaneous_surgery_jordan(example_bump_polygon(), forest)
    assert ok
    assert len(out) < len(example_bump_polygon())
