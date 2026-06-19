"""Directive 028 — multi-gate T054."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.multigate_cluster import (
    audit_multigate_cluster,
    example_four_gate_cluster,
    example_six_gate_nested,
)


@pytest.mark.fast
def test_four_gate_not_auto_protected():
    cluster = example_four_gate_cluster()
    audit = audit_multigate_cluster(cluster)
    assert audit.status == "CONJECTURAL_MULTIGATE_TARGET"
    assert audit.interleaving_unprotected or audit.outcome == "MULTICENTER_RESIDUAL"


@pytest.mark.fast
def test_six_gate_nested():
    cluster = example_six_gate_nested()
    assert cluster.gate_count == 6
    assert cluster.gate_word.pairing == "NESTED"
