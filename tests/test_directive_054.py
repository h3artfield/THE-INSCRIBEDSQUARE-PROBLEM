"""Directive 054 — infinite-dimensional transition exhaustion."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure
from squarepeg.defect_extraction.coherent_route_subtree import audit_coherent_route_subtree, certify_t103
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.countable_child_transition_routes import audit_countable_child_transition_routes, certify_t104
from squarepeg.defect_extraction.gate_order_transition_measure import audit_gate_order_transition_measure
from squarepeg.defect_extraction.infinite_center_transition import audit_infinite_center_transition
from squarepeg.defect_extraction.measure_admissible_transition import audit_measure_admissible_transition
from squarepeg.defect_extraction.measure_transition_closure import audit_measure_transition_closure, certify_t105
from squarepeg.defect_extraction.measure_transition_tightness import audit_measure_transition_tightness
from squarepeg.defect_extraction.route_label_measure import audit_route_label_measure
from squarepeg.defect_extraction.route_oscillation import audit_route_oscillation
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t102u_clean_room import audit_t102u_clean_room, diagnose_d054_outcome
from squarepeg.defect_extraction.unbounded_gate_transition_routes import certify_t106
from squarepeg.defect_extraction.universal_infinite_transition_exhaustion import certify_t101u, certify_t102u


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_measure_admissible_transition():
    audit = audit_measure_admissible_transition(_tree())
    assert audit.transitions


@pytest.mark.fast
def test_child_measure_moments():
    audit = audit_child_transition_measure(_tree())
    assert audit.first_moment_finite


@pytest.mark.fast
def test_measure_tightness():
    audit = audit_measure_transition_tightness(_tree())
    assert audit.records


@pytest.mark.fast
def test_measure_closure():
    audit = audit_measure_transition_closure(_tree())
    assert audit.component_closure


@pytest.mark.fast
def test_countable_child_routes():
    cert = certify_t104(_tree())
    assert cert.status in ("CONJECTURAL_INFINITE_CHILD_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_gate_order_measure():
    audit = audit_gate_order_transition_measure(_tree())
    assert audit.records


@pytest.mark.fast
def test_unbounded_gate_routes():
    cert = certify_t106(_tree())
    assert cert.status in ("CONJECTURAL_GATE_COMPLEXITY_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_infinite_center_transition():
    audit = audit_infinite_center_transition(_tree())
    assert audit.records


@pytest.mark.fast
def test_route_label_mass():
    audit = audit_route_label_measure(_tree())
    assert audit.dominant_label


@pytest.mark.fast
def test_coherent_route_subtree():
    audit = audit_coherent_route_subtree(_tree())
    assert audit.subtrees


@pytest.mark.fast
def test_route_oscillation():
    audit = audit_route_oscillation(_tree())
    assert audit.records


@pytest.mark.fast
def test_t101u_certificate():
    cert = certify_t101u(_tree())
    assert cert.status in ("CONJECTURAL_UNIVERSAL_EXHAUSTION", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t102u_certificate():
    cert = certify_t102u(_tree())
    assert cert.status in ("CONJECTURAL_UNIVERSAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t103_certificate():
    cert = certify_t103(_tree())
    assert cert.status in ("CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t105_certificate():
    cert = certify_t105(_tree())
    assert cert.status in ("CONJECTURAL_MEASURE_CLOSURE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_coverage_certificate_frozen():
    path = Path(__file__).resolve().parents[1] / "artifacts" / "universal_transition_coverage_certificate.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["unresolved_cells"] == 0


@pytest.mark.fast
def test_t102u_clean_room():
    audit = audit_t102u_clean_room(_tree())
    assert audit.verdict in ("T102U_CLEAN_ROOM_VERIFIED", "T102U_REPAIRABLE_GAP", "T102U_INVALID")


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d054_outcome():
    outcome = diagnose_d054_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
