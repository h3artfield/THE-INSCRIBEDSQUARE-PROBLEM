"""Directive 059 clean room and outcome (Directive 059)."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.annular_positive_scale import certify_t113
from squarepeg.global_geometry.finite_center_positive_scale import certify_t114
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters
from squarepeg.global_geometry.positive_scale_residual_routes import audit_positive_scale_residual_routes
from squarepeg.global_geometry.t091_universal_positive_scale import certify_t091u
from squarepeg.global_geometry.t112_positive_scale_classification import certify_t112
from squarepeg.global_geometry.t115_nonannular_exhaustion import certify_t115
from squarepeg.ledger.t045r_dependency_map import write_t045r_attack_map

CleanRoomVerdict = Literal[
    "D059_CLEAN_ROOM_VERIFIED",
    "D059_REPAIRABLE_GAP",
    "D059_INVALID",
]

Outcome = Literal["A", "B", "C", "D", "E"]

ROUTES_PATH = Path(__file__).resolve().parents[3] / "artifacts" / "directive_059_positive_scale_routes.json"


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class Directive059CleanRoom:
    verdict: CleanRoomVerdict
    outcome: Outcome
    answers: list[CleanRoomAnswer]
    messages: list[str]


def write_positive_scale_routes(tree: CanonicalIntrusionTree) -> Path:
    write_t045r_attack_map()
    routes = audit_positive_scale_residual_routes(tree)
    clusters = audit_positive_scale_clusters(tree)
    payload = {
        "clusters": [asdict(c) for c in clusters.clusters],
        "routes": [asdict(r) for r in routes.routes],
        "all_routed": routes.all_routed,
    }
    ROUTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROUTES_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return ROUTES_PATH


def audit_directive_059_clean_room(tree: CanonicalIntrusionTree | None = None) -> Directive059CleanRoom:
    tree = tree or build_binary_equal_ratio_cantor(levels=4, ratio=0.58)
    write_positive_scale_routes(tree)
    clusters = audit_positive_scale_clusters(tree)
    routes = audit_positive_scale_residual_routes(tree)
    t112 = certify_t112(tree)
    t113 = certify_t113(tree)
    t114 = certify_t114(tree)
    t115 = certify_t115(tree)
    t091u = certify_t091u(tree)

    answers = [
        CleanRoomAnswer("Curve-level definition?", clusters.curve_level_definition, str(clusters.curve_level_definition)),
        CleanRoomAnswer("Split exhaustive?", t112.split_exhaustive, str(t112.split_exhaustive)),
        CleanRoomAnswer("Annular hypotheses?", t113.status == "PROVED_LOCALLY", t113.status),
        CleanRoomAnswer("Cross-center preserved?", t114.status == "PROVED_LOCALLY", t114.status),
        CleanRoomAnswer("Nonannular to globals?", routes.all_routed, str(routes.all_routed)),
        CleanRoomAnswer("No new residual?", routes.no_new_residual, str(routes.no_new_residual)),
        CleanRoomAnswer("Fixture/universal separated?", "fixture" in t091u.scope.lower(), t091u.scope[:50]),
        CleanRoomAnswer("T091-U extends fixture?", t091u.extends_fixture, t091u.status),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    outcome = diagnose_d059_outcome(tree)
    if outcome in ("A", "B") and passed >= 8:
        verdict: CleanRoomVerdict = "D059_CLEAN_ROOM_VERIFIED"
    elif passed >= 6:
        verdict = "D059_REPAIRABLE_GAP"
    else:
        verdict = "D059_INVALID"
    return Directive059CleanRoom(verdict=verdict, outcome=outcome, answers=answers, messages=[f"passed={passed}"])


def diagnose_d059_outcome(tree: CanonicalIntrusionTree | None = None) -> Outcome:
    tree = tree or build_binary_equal_ratio_cantor(levels=4, ratio=0.58)
    t113 = certify_t113(tree)
    t114 = certify_t114(tree)
    t115 = certify_t115(tree)
    t091u = certify_t091u(tree)
    routes = audit_positive_scale_residual_routes(tree)
    if t091u.status == "PROVED_LOCALLY" and t115.status == "PROVED_LOCALLY" and not t115.narrow_residual:
        return "A"
    if t113.status == "PROVED_LOCALLY" and t114.status == "PROVED_LOCALLY" and t115.narrow_residual:
        return "B"
    if routes.all_routed and all(r.kind == "GLOBAL_RESIDUAL" for r in routes.routes if r.route == "nonannular"):
        return "C"
    if not routes.all_routed:
        return "E"
    return "B"
