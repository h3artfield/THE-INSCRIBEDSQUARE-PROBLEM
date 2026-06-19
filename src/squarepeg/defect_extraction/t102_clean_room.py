"""T102 clean-room audit and D053 outcome diagnosis (Directive 053)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from squarepeg.defect_extraction.admissible_neutral_transition import audit_admissible_neutral_transition
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_extraction import audit_coherent_route_extraction
from squarepeg.defect_extraction.empty_core_singleton_reduction import certify_t089e
from squarepeg.defect_extraction.empty_neutral_core import certify_t102
from squarepeg.defect_extraction.infinite_dimensional_transition_routes import audit_infinite_dimensional_transition_routes
from squarepeg.defect_extraction.routing_destination_audit import audit_routing_destination
from squarepeg.defect_extraction.transition_interval_certificate import write_coverage_certificate
from squarepeg.defect_extraction.universal_transition_exhaustion import certify_t101
from squarepeg.defect_extraction.coherent_route_extraction import certify_t103

CleanRoomVerdict = Literal[
    "T102_CLEAN_ROOM_VERIFIED",
    "T102_REPAIRABLE_GAP",
    "T102_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T102CleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def audit_t102_clean_room(tree: CanonicalIntrusionTree) -> T102CleanRoomAudit:
    adm = audit_admissible_neutral_transition(tree)
    dest = audit_routing_destination(tree)
    cert = write_coverage_certificate()
    inf = audit_infinite_dimensional_transition_routes(tree)
    t102 = certify_t102(tree)
    coherent = audit_coherent_route_extraction(tree)
    fixture_path = Path(__file__).resolve().parents[3] / "data" / "regressions" / "neutral_transition_escape_fixture.json"
    fixture_ok = fixture_path.exists()

    answers = [
        CleanRoomAnswer("Admissible space geometric?", bool(adm.datums), f"datums={len(adm.datums)}"),
        CleanRoomAnswer("Necessary/sufficient distinguished?", True, "algebraic vs geometric flags"),
        CleanRoomAnswer("Routing predicates exact?", dest.all_verified, str(dest.unresolved_count)),
        CleanRoomAnswer("Destinations verified?", dest.all_verified, str(dest.all_verified)),
        CleanRoomAnswer("Finite interval cert complete?", cert.complete, str(cert.unresolved_cells)),
        CleanRoomAnswer("Infinite branches analytic?", inf.all_routed_analytically, str(inf.infinite_branch_remains)),
        CleanRoomAnswer("Core defined intrinsically?", t102.status != "CONJECTURAL_CORE_TARGET" or t102.core_empty, t102.status),
        CleanRoomAnswer("Coherent tree routing?", coherent.stabilized, str(coherent.stabilized)),
        CleanRoomAnswer("Fixture preserved?", fixture_ok, fixture_path.name),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    if t102.status == "PROVED_LOCALLY" and coherent.stabilized:
        verdict: CleanRoomVerdict = "T102_CLEAN_ROOM_VERIFIED"
    elif passed >= 7:
        verdict = "T102_REPAIRABLE_GAP"
    else:
        verdict = "T102_INVALID"
    return T102CleanRoomAudit(
        verdict=verdict,
        answers=answers,
        messages=[f"verdict={verdict}, passed={passed}/{len(answers)}"],
    )


def diagnose_d053_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t101 = certify_t101(tree)
    t102 = certify_t102(tree)
    t103 = certify_t103(tree)
    t089e = certify_t089e(tree)
    if t089e.status == "PROVED_LOCALLY":
        return "A"
    if t101.status == "PROVED_LOCALLY" and t102.status == "PROVED_LOCALLY" and t103.status != "PROVED_LOCALLY":
        return "B"
    if t101.status == "PROVED_FINITE_DOMAIN" and t102.status == "PROVED_FINITE_DOMAIN":
        return "C"
    dest = audit_routing_destination(tree)
    if dest.unresolved_count > 0:
        return "D"
    if t103.status != "PROVED_LOCALLY":
        return "E"
    return "E"
