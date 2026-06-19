"""Directive 028 — cluster forest."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.cluster_forest import build_cluster_forest
from squarepeg.defect_extraction.cluster_signature import certify_t052
from squarepeg.defect_extraction.dirty_examples import example_dirty_saturatable_two_gate


@pytest.mark.fast
def test_cluster_forest_laminar():
    _, cluster, _ = example_dirty_saturatable_two_gate()
    forest = build_cluster_forest([cluster])
    assert forest.laminar
    cert = certify_t052(forest, [], 0, 1)
    assert cert.cluster_carleson.max_cluster_diameter > 0
