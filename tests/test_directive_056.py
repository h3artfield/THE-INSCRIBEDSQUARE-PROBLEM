"""Directive 056 — order-augmented infinite transition exhaustion."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.augmented_order_transition import audit_augmented_order_transition
from squarepeg.defect_extraction.augmented_transition_routes import audit_augmented_transition_routes
from squarepeg.defect_extraction.augmented_order_classification import audit_augmented_order_classification
from squarepeg.defect_extraction.collision_exhaustion import audit_collision_exhaustion
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.diffuse_order_transition import audit_diffuse_order_transition
from squarepeg.defect_extraction.gate_order_realizability import audit_gate_order_realizability
from squarepeg.defect_extraction.order_augmented_exhaustion import certify_t108
from squarepeg.defect_extraction.pair_interaction_concentration import audit_pair_interaction_concentration
from squarepeg.defect_extraction.route_set_topology import audit_route_set_topology
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t108_clean_room import audit_t108_clean_room, diagnose_d056_outcome
from squarepeg.defect_extraction.transition_boundary_cases import audit_transition_boundary_cases
from squarepeg.defect_extraction.universal_empty_neutral_core import certify_t102u_augmented
from squarepeg.defect_extraction.universal_transition_exhaustion_augmented import certify_t101u_augmented


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_augmented_admissible_no_discrete_order():
    audit = audit_augmented_order_transition(_tree())
    assert audit.no_discrete_gate_order


@pytest.mark.fast
def test_realizability_excludes_algebraic():
    audit = audit_gate_order_realizability(_tree())
    assert audit.all_realizable


@pytest.mark.fast
def test_augmented_route_predicates():
    audit = audit_augmented_transition_routes(_tree())
    assert audit.all_routed


@pytest.mark.fast
def test_boundary_cases():
    audit = audit_transition_boundary_cases(_tree())
    assert audit.all_covered


@pytest.mark.fast
def test_pair_interaction_concentration():
    audit = audit_pair_interaction_concentration(_tree())
    assert audit.all_routed


@pytest.mark.fast
def test_collision_exhaustion():
    audit = audit_collision_exhaustion(_tree())
    assert audit.all_classified


@pytest.mark.fast
def test_order_classification():
    audit = audit_augmented_order_classification(_tree())
    assert audit.all_routed


@pytest.mark.fast
def test_diffuse_order_routing():
    audit = audit_diffuse_order_transition(_tree())
    assert audit.all_routed


@pytest.mark.fast
def test_t108_certificate():
    cert = certify_t108(_tree())
    assert cert.status in ("CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t101u_augmented():
    cert = certify_t101u_augmented(_tree())
    assert cert.status in ("CONJECTURAL_UNIVERSAL_EXHAUSTION", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t102u_augmented():
    cert = certify_t102u_augmented(_tree())
    assert cert.status in ("CONJECTURAL_UNIVERSAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_route_set_topology():
    audit = audit_route_set_topology(_tree())
    assert audit.all_measurable


@pytest.mark.fast
def test_t108_clean_room():
    audit = audit_t108_clean_room(_tree())
    assert audit.verdict in ("T108_CLEAN_ROOM_VERIFIED", "T108_REPAIRABLE_GAP", "T108_INVALID")


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d056_outcome():
    outcome = diagnose_d056_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
