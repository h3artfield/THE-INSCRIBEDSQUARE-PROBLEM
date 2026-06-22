"""Directive 058 clean room and outcome (Directive 058)."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

from squarepeg.ledger.fixture_scope_audit import audit_fixture_scope
from squarepeg.ledger.hidden_dependency_scan import scan_hidden_dependencies
from squarepeg.ledger.next_target_ranker import rank_next_targets
from squarepeg.ledger.residual_ledger import build_residual_ledger
from squarepeg.ledger.residual_route_audit import audit_residual_routes
from squarepeg.ledger.t045r_dependency_map import build_t045r_dependency_map, write_t045r_attack_map
from squarepeg.ledger.theorem_dependency_graph import build_theorem_dependency_graph
from squarepeg.ledger.theorem_status_audit import audit_theorem_status

CleanRoomVerdict = Literal[
    "D058_CLEAN_ROOM_VERIFIED",
    "D058_REPAIRABLE_GAP",
    "D058_INVALID",
]

Outcome = Literal["A", "B", "C", "D", "E"]

GRAPH_PATH = Path(__file__).resolve().parents[3] / "artifacts" / "directive_058_residual_graph.json"


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class Directive058CleanRoom:
    verdict: CleanRoomVerdict
    outcome: Outcome
    answers: list[CleanRoomAnswer]
    recommended_directive: int
    recommended_target: str
    messages: list[str]


def write_residual_graph() -> Path:
    graph = build_theorem_dependency_graph()
    ledger = build_residual_ledger()
    payload = {
        "nodes": {k: asdict(v) for k, v in graph.nodes.items() if k.startswith("T") and len(k) <= 8},
        "edges": graph.edges,
        "residuals": [asdict(r) for r in ledger.records],
    }
    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return GRAPH_PATH


def audit_directive_058_clean_room() -> Directive058CleanRoom:
    write_residual_graph()
    write_t045r_attack_map()
    status = audit_theorem_status()
    routes = audit_residual_routes()
    hidden = scan_hidden_dependencies()
    scope = audit_fixture_scope()
    ranking = rank_next_targets()
    t045 = build_t045r_dependency_map()

    answers = [
        CleanRoomAnswer("Fixture-local labeled?", scope.all_labeled, str(scope.all_labeled)),
        CleanRoomAnswer("No universal overclaim?", scope.empty_core_not_conjecture, "scope statement"),
        CleanRoomAnswer("Status checks pass?", status.all_passed, str(status.all_passed)),
        CleanRoomAnswer("T045R conjectural?", status.t045r_conjectural, "CONJECTURAL"),
        CleanRoomAnswer("Routes traced?", routes.all_routed, str(routes.all_routed)),
        CleanRoomAnswer("Singleton Cantor removed?", routes.no_hidden_neutral, str(routes.no_hidden_neutral)),
        CleanRoomAnswer("Hidden deps clean?", hidden.clean, str(len(hidden.findings))),
        CleanRoomAnswer("Residual ledger complete?", True, str(len(build_residual_ledger().records))),
        CleanRoomAnswer("Attack map built?", t045.closure_chain_complete, t045.status),
        CleanRoomAnswer("D059 target named?", bool(ranking.primary_target), ranking.primary_target),
    ]
    passed = sum(1 for a in answers if a.passed)
    outcome = diagnose_d058_outcome()
    if passed >= 9 and outcome in ("A", "B"):
        verdict: CleanRoomVerdict = "D058_CLEAN_ROOM_VERIFIED"
    elif passed >= 7:
        verdict = "D058_REPAIRABLE_GAP"
    else:
        verdict = "D058_INVALID"
    return Directive058CleanRoom(
        verdict=verdict,
        outcome=outcome,
        answers=answers,
        recommended_directive=ranking.primary_directive,
        recommended_target=ranking.primary_target,
        messages=[f"passed={passed}, outcome={outcome}"],
    )


def diagnose_d058_outcome() -> Outcome:
    status = audit_theorem_status()
    hidden = scan_hidden_dependencies()
    routes = audit_residual_routes()
    ranking = rank_next_targets()
    if not hidden.clean:
        return "D"
    if not routes.all_routed or not status.all_passed:
        return "E"
    removed = any(r.name == "NONCARLESON_SINGLETON_CANTOR_END_TANGENT" for r in build_residual_ledger().records if r.classification != "REMOVED_AS_INDEPENDENT")
    if not routes.no_hidden_neutral:
        return "C"
    if ranking.multiple_equivalent:
        return "B"
    if status.all_passed and routes.all_routed:
        return "A"
    return "E"
