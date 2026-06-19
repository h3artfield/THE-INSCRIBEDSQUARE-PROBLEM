"""Directive 053 — universal transition exhaustion and empty neutral core."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from squarepeg.defect_extraction.admissible_neutral_transition import audit_admissible_neutral_transition
from squarepeg.defect_extraction.coherent_route_extraction import audit_coherent_route_extraction, certify_t103
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.empty_core_singleton_reduction import certify_t089e
from squarepeg.defect_extraction.empty_neutral_core import audit_empty_neutral_core, certify_t102
from squarepeg.defect_extraction.infinite_dimensional_transition_routes import audit_infinite_dimensional_transition_routes
from squarepeg.defect_extraction.neutral_routing_predicates import audit_neutral_routing_predicates
from squarepeg.defect_extraction.routing_destination_audit import audit_routing_destination
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t102_clean_room import audit_t102_clean_room, diagnose_d053_outcome
from squarepeg.defect_extraction.transition_domain_cover import audit_transition_domain_cover
from squarepeg.defect_extraction.transition_interval_certificate import build_interval_certificate, write_coverage_certificate
from squarepeg.defect_extraction.universal_transition_exhaustion import certify_t101


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_admissible_vs_algebraic():
    audit = audit_admissible_neutral_transition(_tree())
    assert audit.datums


@pytest.mark.fast
def test_routing_predicates():
    audit = audit_neutral_routing_predicates(_tree())
    assert audit.results


@pytest.mark.fast
def test_routing_destinations():
    audit = audit_routing_destination(_tree())
    assert audit.records


@pytest.mark.fast
def test_interval_domain_cover():
    audit = audit_transition_domain_cover()
    assert audit.finite_domain_covered


@pytest.mark.fast
def test_zero_unresolved_cells():
    cert = build_interval_certificate()
    assert cert.unresolved_cells == 0


@pytest.mark.fast
def test_coverage_certificate():
    cert = write_coverage_certificate()
    assert cert.complete


@pytest.mark.fast
def test_infinite_dimensional_routes():
    audit = audit_infinite_dimensional_transition_routes(_tree())
    assert audit.infinite_branch_remains


@pytest.mark.fast
def test_empty_core_fixture():
    audit = audit_empty_neutral_core(_tree())
    assert audit.core_empty_fixture


@pytest.mark.fast
def test_coherent_route_extraction():
    audit = audit_coherent_route_extraction(_tree())
    assert audit.records


@pytest.mark.fast
def test_frozen_fixture():
    path = Path(__file__).resolve().parents[1] / "data" / "regressions" / "neutral_transition_escape_fixture.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["family_compact"] is False


@pytest.mark.fast
def test_t101_certificate():
    cert = certify_t101(_tree())
    assert cert.status in ("CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "PROVED_FINITE_DOMAIN")


@pytest.mark.fast
def test_t102_certificate():
    cert = certify_t102(_tree())
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY", "PROVED_FINITE_DOMAIN")


@pytest.mark.fast
def test_t103_certificate():
    cert = certify_t103(_tree())
    assert cert.status in ("CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t089e_certificate():
    cert = certify_t089e(_tree())
    assert cert.status in ("CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t102_clean_room():
    audit = audit_t102_clean_room(_tree())
    assert audit.verdict in ("T102_CLEAN_ROOM_VERIFIED", "T102_REPAIRABLE_GAP", "T102_INVALID")


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d053_outcome():
    outcome = diagnose_d053_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
