"""Directive 055 — gate-order measures and weak closure."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from squarepeg.defect_extraction.augmented_order_transition import audit_augmented_order_transition
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.countable_child_transition_routes import certify_t104
from squarepeg.defect_extraction.cyclic_gate_measure import audit_cyclic_gate_measure
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.defect_extraction.gate_measure_tightness import audit_gate_measure_tightness
from squarepeg.defect_extraction.gate_measure_weak_closure import audit_gate_measure_weak_closure, certify_t107
from squarepeg.defect_extraction.gate_order_realizability import audit_gate_order_realizability
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure
from squarepeg.defect_extraction.order_augmented_exhaustion import certify_t108
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t105r_clean_room import audit_t105r_clean_room, diagnose_d055_outcome
from squarepeg.defect_extraction.t105r_measure_closure import certify_t105r
from squarepeg.defect_extraction.unbounded_gate_transition_routes import certify_t106


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_marked_gate_measure():
    audit = audit_marked_gate_measure(_tree())
    assert audit.measures


@pytest.mark.fast
def test_cyclic_seam_independence():
    audit = audit_cyclic_gate_measure(_tree())
    assert audit.seam_independent


@pytest.mark.fast
def test_pair_reconstruction():
    audit = audit_gate_pair_interaction_measure(_tree())
    assert audit.exact_reconstruction


@pytest.mark.fast
def test_gate_collisions():
    audit = audit_gate_collision_measure(_tree())
    assert audit.measures is not None


@pytest.mark.fast
def test_gate_measure_tightness():
    audit = audit_gate_measure_tightness(_tree())
    assert audit.all_tight


@pytest.mark.fast
def test_weak_closure():
    audit = audit_gate_measure_weak_closure(_tree())
    assert audit.discrete_gate_order_eliminated


@pytest.mark.fast
def test_augmented_order_transition():
    audit = audit_augmented_order_transition(_tree())
    assert audit.no_discrete_gate_order


@pytest.mark.fast
def test_realizability():
    audit = audit_gate_order_realizability(_tree())
    assert audit.records


@pytest.mark.fast
def test_t107_certificate():
    cert = certify_t107(_tree())
    assert cert.status in ("CONJECTURAL_GATE_MEASURE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t105r_certificate():
    cert = certify_t105r(_tree())
    assert cert.status in ("CONJECTURAL_MEASURE_CLOSURE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t108_certificate():
    cert = certify_t108(_tree())
    assert cert.status in ("CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t104_revalidated():
    assert certify_t104(_tree()).status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_t106_revalidated():
    assert certify_t106(_tree()).status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_gate_order_fixture():
    path = Path(__file__).resolve().parents[1] / "data" / "regressions" / "gate_order_weak_closure_fixture.json"
    if not path.exists():
        audit_t105r_clean_room(_tree())
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["failure"]


@pytest.mark.fast
def test_t105r_clean_room():
    audit = audit_t105r_clean_room(_tree())
    assert audit.verdict in ("T105R_CLEAN_ROOM_VERIFIED", "T105R_REPAIRABLE_GAP", "T105R_INVALID")


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d055_outcome():
    outcome = diagnose_d055_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
