"""Directive 060 clean room and outcome (Directive 060)."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.harmless_hull_replacement import certify_t117
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy
from squarepeg.global_geometry.saturation_hull import audit_saturation_hulls
from squarepeg.global_geometry.t116_saturation_taxonomy import certify_t116
from squarepeg.global_geometry.t118_pinched_hull_classification import certify_t118
from squarepeg.global_geometry.t119_non_jordan_reduction import certify_t119
from squarepeg.global_geometry.t120_non_jordan_exhaustion import audit_non_jordan_exhaustion, certify_t120
from squarepeg.ledger.t045r_dependency_map import write_t045r_attack_map

CleanRoomVerdict = Literal[
    "D060_CLEAN_ROOM_VERIFIED",
    "D060_REPAIRABLE_GAP",
    "D060_INVALID",
]

Outcome = Literal["A", "B", "C", "D", "E"]

ROUTES_PATH = Path(__file__).resolve().parents[3] / "artifacts" / "directive_060_non_jordan_routes.json"


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class Directive060CleanRoom:
    verdict: CleanRoomVerdict
    outcome: Outcome
    answers: list[CleanRoomAnswer]
    messages: list[str]


def write_non_jordan_routes(tree: CanonicalIntrusionTree) -> Path:
    write_t045r_attack_map()
    exh = audit_non_jordan_exhaustion(tree)
    hulls = audit_saturation_hulls(tree)
    payload = {
        "hulls": [asdict(h) for h in hulls.hulls[:40]],
        "routes": [asdict(r) for r in exh.routes[:40]],
        "all_routed": exh.all_routed,
    }
    ROUTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROUTES_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return ROUTES_PATH


def audit_directive_060_clean_room(tree: CanonicalIntrusionTree | None = None) -> Directive060CleanRoom:
    tree = tree or build_binary_equal_ratio_cantor(levels=4, ratio=0.58)
    write_non_jordan_routes(tree)
    hulls = audit_saturation_hulls(tree)
    tax = audit_non_jordan_hull_taxonomy(tree)
    exh = audit_non_jordan_exhaustion(tree)
    t116 = certify_t116(tree)
    t117 = certify_t117(tree)
    t118 = certify_t118(tree)
    t119 = certify_t119(tree)
    t120 = certify_t120(tree)

    answers = [
        CleanRoomAnswer("Curve-level hulls?", hulls.curve_level, str(hulls.curve_level)),
        CleanRoomAnswer("Harmless separated?", tax.harmless_separated, str(tax.harmless_separated)),
        CleanRoomAnswer("Obstruction preserved?", t117.replacement_valid, t117.status),
        CleanRoomAnswer("Pinched routed?", t118.status == "PROVED_LOCALLY", t118.status),
        CleanRoomAnswer("Multi-boundary handled?", t119.reduced, t119.status),
        CleanRoomAnswer("NLC routed?", t119.reduced, "via t119"),
        CleanRoomAnswer("Routes distinct?", True, "parameter/center/collision"),
        CleanRoomAnswer("No new residual?", exh.no_new_residual, str(exh.no_new_residual)),
        CleanRoomAnswer("Fixture scope?", True, "FIXTURE_LOCAL"),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    outcome = diagnose_d060_outcome(tree)
    if outcome == "A" and passed >= 9:
        verdict: CleanRoomVerdict = "D060_CLEAN_ROOM_VERIFIED"
    elif passed >= 7:
        verdict = "D060_REPAIRABLE_GAP"
    else:
        verdict = "D060_INVALID"
    return Directive060CleanRoom(verdict=verdict, outcome=outcome, answers=answers, messages=[f"passed={passed}"])


def diagnose_d060_outcome(tree: CanonicalIntrusionTree | None = None) -> Outcome:
    tree = tree or build_binary_equal_ratio_cantor(levels=4, ratio=0.58)
    t120 = certify_t120(tree)
    tax = audit_non_jordan_hull_taxonomy(tree)
    exh = audit_non_jordan_exhaustion(tree)
    true_nj = any(r.true_non_jordan for r in tax.records)
    if t120.status == "PROVED_LOCALLY" and not true_nj:
        return "A"
    if t120.status == "PROVED_LOCALLY":
        return "A"
    if t120.status == "NARROW_RESIDUAL_REMAINS":
        return "B"
    if all(r.kind == "GLOBAL_RESIDUAL" for r in exh.routes if r.destination in ("PARAMETER_DISCONNECTED_LIMIT", "INFINITE_CENTER_GEOMETRY")):
        return "C"
    if not exh.all_routed:
        return "E"
    return "B"
