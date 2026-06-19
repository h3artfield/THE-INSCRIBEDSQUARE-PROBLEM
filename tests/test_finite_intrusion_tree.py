"""Directive 028 — finite intrusion tree T050."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.dirty_examples import dirty_lobe_intrusions
from squarepeg.defect_extraction.finite_intrusion_tree import classify_finite_intrusion_tree


@pytest.mark.fast
def test_finite_tree_two_gate():
    boundary = [(1.0, 0.0), (1.5, 0.35), (2.0, 0.0)]
    retained = [(0, 0), (3, 0), (3, 3), (0, 3)]
    audit = classify_finite_intrusion_tree((0.15, 0.45), boundary, dirty_lobe_intrusions(), retained)
    assert audit.outcome == "TWO_GATE_CLEAN"
    assert audit.status == "PROVED_LOCALLY_FINITE_TREE"
