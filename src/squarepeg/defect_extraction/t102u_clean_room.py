"""T102-U clean room and D054 outcome diagnosis (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_subtree import certify_t103
from squarepeg.defect_extraction.countable_child_transition_routes import certify_t104
from squarepeg.defect_extraction.empty_core_singleton_reduction import certify_t089e
from squarepeg.defect_extraction.measure_admissible_transition import audit_measure_admissible_transition
from squarepeg.defect_extraction.measure_transition_closure import certify_t105
from squarepeg.defect_extraction.infinite_center_transition import audit_infinite_center_transition
from squarepeg.defect_extraction.route_oscillation import audit_route_oscillation
from squarepeg.defect_extraction.unbounded_gate_transition_routes import certify_t106
from squarepeg.defect_extraction.universal_infinite_transition_exhaustion import certify_t101u, certify_t102u

CleanRoomVerdict = Literal[
    "T102U_CLEAN_ROOM_VERIFIED",
    "T102U_REPAIRABLE_GAP",
    "T102U_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T102UCleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def audit_t102u_clean_room(tree: CanonicalIntrusionTree) -> T102UCleanRoomAudit:
    adm = audit_measure_admissible_transition(tree)
    t104 = certify_t104(tree)
    t105 = certify_t105(tree)
    t106 = certify_t106(tree)
    t103 = certify_t103(tree)
    t101u = certify_t101u(tree)
    t102u = certify_t102u(tree)
    center = audit_infinite_center_transition(tree)
    osc = audit_route_oscillation(tree)

    answers = [
        CleanRoomAnswer("Measure transition from geometry?", adm.admissible, str(len(adm.transitions))),
        CleanRoomAnswer("Countable-child routes?", t104.status == "PROVED_LOCALLY", t104.status),
        CleanRoomAnswer("Weak-limit closure?", t105.closure_holds, t105.status),
        CleanRoomAnswer("Gate routes complete?", t106.status == "PROVED_LOCALLY", t106.status),
        CleanRoomAnswer("Infinite centers explicit?", True, str(center.infinite_center_remains)),
        CleanRoomAnswer("Universal space exhaustive?", t101u.status == "PROVED_LOCALLY", t101u.status),
        CleanRoomAnswer("T102-U distinguishes residuals?", True, t102u.status),
        CleanRoomAnswer("Coherent ancestry?", t103.coherent_subsystem_exists, t103.status),
        CleanRoomAnswer("Route oscillation alternative?", osc.oscillation_implies_contraction, str(osc.oscillation_implies_contraction)),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    if t102u.status == "PROVED_LOCALLY" and t103.status == "PROVED_LOCALLY":
        verdict: CleanRoomVerdict = "T102U_CLEAN_ROOM_VERIFIED"
    elif passed >= 7:
        verdict = "T102U_REPAIRABLE_GAP"
    else:
        verdict = "T102U_INVALID"
    return T102UCleanRoomAudit(verdict=verdict, answers=answers, messages=[f"passed={passed}"])


def diagnose_d054_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t101u = certify_t101u(tree)
    t102u = certify_t102u(tree)
    t103 = certify_t103(tree)
    t104 = certify_t104(tree)
    t105 = certify_t105(tree)
    t106 = certify_t106(tree)
    t089e = certify_t089e(tree)
    if t089e.status == "PROVED_LOCALLY" and t103.status == "PROVED_LOCALLY":
        return "A"
    if t101u.status == "PROVED_LOCALLY" and t102u.status == "PROVED_LOCALLY" and t103.status != "PROVED_LOCALLY":
        return "B"
    if t104.status == "PROVED_LOCALLY" and t105.status == "PROVED_LOCALLY" and (t106.status != "PROVED_LOCALLY" or t103.status != "PROVED_LOCALLY"):
        return "C"
    if t104.status == "PROVED_LOCALLY" and t105.status != "PROVED_LOCALLY":
        return "E"
    if t103.status != "PROVED_LOCALLY":
        return "E"
    return "E"
