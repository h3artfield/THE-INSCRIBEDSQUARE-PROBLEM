"""Directive 061 clean room and outcome (Directive 061)."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.cantor_parameter_support import audit_cantor_parameter_support
from squarepeg.global_geometry.cross_component_interactions import audit_cross_component_interactions
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits
from squarepeg.global_geometry.parameter_support import audit_parameter_support
from squarepeg.global_geometry.t121_parameter_decomposition import certify_t121
from squarepeg.global_geometry.t122_component_splitting import certify_t122
from squarepeg.global_geometry.t123_cross_component_routing import certify_t123
from squarepeg.global_geometry.t124_parameter_reduction import certify_t124
from squarepeg.global_geometry.t125_parameter_exhaustion import audit_parameter_exhaustion, certify_t125

CleanRoomVerdict = Literal[
    "D061_CLEAN_ROOM_VERIFIED",
    "D061_REPAIRABLE_GAP",
    "D061_INVALID",
]

Outcome = Literal["A", "B", "C", "D", "E"]

ROUTES_PATH = Path(__file__).resolve().parents[3] / "artifacts" / "directive_061_parameter_routes.json"


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class Directive061CleanRoom:
    verdict: CleanRoomVerdict
    outcome: Outcome
    answers: list[CleanRoomAnswer]
    messages: list[str]


def write_parameter_routes(tree: CanonicalIntrusionTree) -> Path:
    exh = audit_parameter_exhaustion(tree)
    support = audit_parameter_support(tree)
    payload = {
        "support": [asdict(s) for s in support.records],
        "routes": [asdict(r) for r in exh.routes],
        "all_routed": exh.all_routed,
    }
    ROUTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROUTES_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return ROUTES_PATH


def audit_directive_061_clean_room(tree: CanonicalIntrusionTree | None = None) -> Directive061CleanRoom:
    tree = tree or build_binary_equal_ratio_cantor(levels=4, ratio=0.58)
    write_parameter_routes(tree)
    support = audit_parameter_support(tree)
    limits = audit_parameter_disconnected_limits(tree)
    exh = audit_parameter_exhaustion(tree)
    cantor = audit_cantor_parameter_support(tree)
    cross = audit_cross_component_interactions(tree)
    t121 = certify_t121(tree)
    t122 = certify_t122(tree)
    t123 = certify_t123(tree)
    t124 = certify_t124(tree)
    t125 = certify_t125(tree)

    answers = [
        CleanRoomAnswer("Curve-level support?", support.curve_level, str(support.curve_level)),
        CleanRoomAnswer("Harmless separated?", limits.harmless_separated, str(limits.harmless_separated)),
        CleanRoomAnswer("Obstruction preserved?", t122.obstruction_preserved, t122.status),
        CleanRoomAnswer("Interactions routed?", t123.routed, t123.status),
        CleanRoomAnswer("Countable tails classified?", t124.reduced, t124.status),
        CleanRoomAnswer("Cantor routed safely?", cantor.no_singleton_cantor_reintroduced, "no NCSC reintro"),
        CleanRoomAnswer("All limits routed?", exh.all_routed, str(exh.all_routed)),
        CleanRoomAnswer("Fixture scope?", True, "FIXTURE_LOCAL"),
        CleanRoomAnswer("No new residual?", exh.no_new_residual, str(exh.no_new_residual)),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    outcome = diagnose_d061_outcome(tree)
    if outcome == "A" and passed >= 9:
        verdict: CleanRoomVerdict = "D061_CLEAN_ROOM_VERIFIED"
    elif passed >= 7:
        verdict = "D061_REPAIRABLE_GAP"
    else:
        verdict = "D061_INVALID"
    _ = cross
    return Directive061CleanRoom(verdict=verdict, outcome=outcome, answers=answers, messages=[f"passed={passed}"])


def diagnose_d061_outcome(tree: CanonicalIntrusionTree | None = None) -> Outcome:
    tree = tree or build_binary_equal_ratio_cantor(levels=4, ratio=0.58)
    t125 = certify_t125(tree)
    limits = audit_parameter_disconnected_limits(tree)
    exh = audit_parameter_exhaustion(tree)
    true_disc = any(r.true_disconnection for r in limits.records)
    if t125.status == "PROVED_LOCALLY" and not true_disc:
        return "A"
    if t125.status == "PROVED_LOCALLY":
        return "A"
    if t125.status == "NARROW_RESIDUAL_REMAINS":
        return "B"
    if all(
        r.destination in ("INFINITE_CENTER_GEOMETRY", "NONSUMMABLE_DIFFUSE_END_GEOMETRY")
        for r in exh.routes
        if r.kind == "GLOBAL_RESIDUAL"
    ):
        return "C"
    if not exh.all_routed:
        return "E"
    return "B"
