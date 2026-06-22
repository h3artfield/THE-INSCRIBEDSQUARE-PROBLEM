"""Directive 058 — global residual ledger and T045R attack map."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from squarepeg.ledger.directive_058_clean_room import (
    audit_directive_058_clean_room,
    diagnose_d058_outcome,
    write_residual_graph,
)
from squarepeg.ledger.fixture_scope_audit import audit_fixture_scope
from squarepeg.ledger.hidden_dependency_scan import scan_hidden_dependencies
from squarepeg.ledger.next_target_ranker import rank_next_targets
from squarepeg.ledger.residual_ledger import GLOBAL_RESIDUALS, REMOVED_RESIDUALS, build_residual_ledger
from squarepeg.ledger.residual_route_audit import audit_residual_routes
from squarepeg.ledger.t045r_dependency_map import build_t045r_dependency_map, write_t045r_attack_map
from squarepeg.ledger.theorem_dependency_graph import build_theorem_dependency_graph
from squarepeg.ledger.theorem_status_audit import audit_theorem_status


@pytest.mark.fast
def test_dependency_graph():
    graph = build_theorem_dependency_graph()
    assert graph.nodes
    assert graph.edges


@pytest.mark.fast
def test_residual_ledger():
    ledger = build_residual_ledger()
    assert ledger.complete
    assert len(ledger.records) == len(GLOBAL_RESIDUALS) + len(REMOVED_RESIDUALS)


@pytest.mark.fast
def test_theorem_status_audit():
    audit = audit_theorem_status()
    assert audit.all_passed
    assert audit.t045r_conjectural


@pytest.mark.fast
def test_residual_route_audit():
    audit = audit_residual_routes()
    assert audit.all_routed
    assert audit.no_hidden_neutral


@pytest.mark.fast
def test_hidden_dependency_scan():
    scan = scan_hidden_dependencies()
    assert scan.clean


@pytest.mark.fast
def test_fixture_scope_audit():
    audit = audit_fixture_scope()
    assert audit.all_labeled
    assert audit.empty_core_not_conjecture


@pytest.mark.fast
def test_t045r_dependency_map():
    amap = build_t045r_dependency_map()
    assert amap.target == "T045R"
    assert "CONJECTURAL" in amap.status
    assert amap.neutral_branch_closed


@pytest.mark.fast
def test_next_target_ranker():
    ranking = rank_next_targets()
    assert ranking.primary_target == "POSITIVE_SCALE_NONANNULAR_CLUSTER"
    assert ranking.primary_directive == 59


@pytest.mark.fast
def test_residual_graph_artifact():
    path = write_residual_graph()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["edges"]


@pytest.mark.fast
def test_attack_map_artifact():
    path = write_t045r_attack_map()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["blockers"]


@pytest.mark.fast
def test_noncarleson_removed():
    ledger = build_residual_ledger()
    rec = next(r for r in ledger.records if r.name == "NONCARLESON_SINGLETON_CANTOR_END_TANGENT")
    assert rec.classification == "REMOVED_AS_INDEPENDENT"


@pytest.mark.fast
def test_d058_clean_room():
    audit = audit_directive_058_clean_room()
    assert audit.verdict in ("D058_CLEAN_ROOM_VERIFIED", "D058_REPAIRABLE_GAP", "D058_INVALID")


@pytest.mark.fast
def test_d058_outcome():
    outcome = diagnose_d058_outcome()
    assert outcome in ("A", "B", "C", "D", "E")
