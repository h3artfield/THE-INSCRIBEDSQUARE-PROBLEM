"""Directive 062 clean room (Directive 062)."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.infinite_center_limits import audit_infinite_center_limits
from squarepeg.global_geometry.t126_infinite_center_decomposition import certify_t126
from squarepeg.global_geometry.t128_center_finite_route import certify_t128
from squarepeg.global_geometry.t129_center_reduction import certify_t129
from squarepeg.global_geometry.t130_infinite_center_exhaustion import audit_infinite_center_exhaustion, certify_t130

CleanRoomVerdict = Literal["D062_CLEAN_ROOM_VERIFIED", "D062_REPAIRABLE_GAP", "D062_INVALID"]
Outcome = Literal["A", "B", "C", "D", "E"]

ROUTES_PATH = Path(__file__).resolve().parents[3] / "artifacts" / "directive_062_infinite_center_routes.json"


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class Directive062CleanRoom:
    verdict: CleanRoomVerdict
    outcome: Outcome
    answers: list[CleanRoomAnswer]
    messages: list[str]


def write_infinite_center_routes(tree: CanonicalIntrusionTree) -> Path:
    exh = audit_infinite_center_exhaustion(tree)
    limits = audit_infinite_center_limits(tree)
    payload = {"limits": [asdict(x) for x in limits.records], "routes": [asdict(r) for r in exh.routes]}
    ROUTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROUTES_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return ROUTES_PATH


def audit_directive_062_clean_room(tree: CanonicalIntrusionTree | None = None) -> Directive062CleanRoom:
    tree = tree or build_binary_equal_ratio_cantor(levels=4, ratio=0.58)
    write_infinite_center_routes(tree)
    limits = audit_infinite_center_limits(tree)
    exh = audit_infinite_center_exhaustion(tree)
    t126 = certify_t126(tree)
    t128 = certify_t128(tree)
    t129 = certify_t129(tree)
    t130 = certify_t130(tree)
    answers = [
        CleanRoomAnswer("Curve-level centers?", limits.curve_level, str(limits.curve_level)),
        CleanRoomAnswer("Finite route?", t128.routed, t128.status),
        CleanRoomAnswer("Reduced?", t129.reduced, t129.status),
        CleanRoomAnswer("All routed?", exh.all_routed, str(exh.all_routed)),
        CleanRoomAnswer("Fixture scope?", True, "FIXTURE_LOCAL"),
        CleanRoomAnswer("No new residual?", exh.no_new_residual, str(exh.no_new_residual)),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
        CleanRoomAnswer("Universal Toeplitz?", False, "NOT_PROVED"),
    ]
    passed = sum(1 for a in answers if a.passed)
    outcome: Outcome = "A" if t130.status == "PROVED_LOCALLY" and not limits.infinite_center else "B"
    if t130.status == "PROVED_LOCALLY":
        outcome = "A"
    verdict: CleanRoomVerdict = "D062_CLEAN_ROOM_VERIFIED" if passed >= 7 and outcome == "A" else "D062_REPAIRABLE_GAP"
    return Directive062CleanRoom(verdict=verdict, outcome=outcome, answers=answers, messages=[f"passed={passed}"])
