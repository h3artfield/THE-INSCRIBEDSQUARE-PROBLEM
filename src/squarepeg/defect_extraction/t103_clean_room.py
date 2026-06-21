"""T103 clean room and D057 outcome (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_order_transition import audit_augmented_order_transition
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_subsystem import audit_coherent_route_subsystem
from squarepeg.defect_extraction.route_constant_uniformity import audit_route_constant_uniformity, certify_t110
from squarepeg.defect_extraction.route_density_tree import certify_t109
from squarepeg.defect_extraction.route_oscillation_cost import audit_route_oscillation_cost
from squarepeg.defect_extraction.route_oscillation_reduction import certify_t111
from squarepeg.defect_extraction.route_responsibility import audit_route_responsibility
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass
from squarepeg.defect_extraction.t089e_reduction import certify_t089e_coherent
from squarepeg.defect_extraction.t103_coherent_route import certify_t103_coherent

CleanRoomVerdict = Literal[
    "T103_CLEAN_ROOM_VERIFIED",
    "T103_REPAIRABLE_GAP",
    "T103_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T103CleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def audit_t103_clean_room(tree: CanonicalIntrusionTree) -> T103CleanRoomAudit:
    resp = audit_route_responsibility(tree)
    mass = audit_route_signature_mass(tree)
    subsystem = audit_coherent_route_subsystem(tree)
    osc = audit_route_oscillation_cost(tree)
    constants = audit_route_constant_uniformity(tree)
    t103 = certify_t103_coherent(tree)
    t089e = certify_t089e_coherent(tree)
    t109 = certify_t109(tree)
    t110 = certify_t110(tree)
    t111 = certify_t111(tree)
    aug = audit_augmented_order_transition(tree)

    answers = [
        CleanRoomAnswer("Signature preserving?", resp.signature_preserving, str(resp.signature_preserving)),
        CleanRoomAnswer("No double count?", resp.no_double_count, str(resp.no_double_count)),
        CleanRoomAnswer("Slice dominance ancestry?", subsystem.ancestry_compatible, str(subsystem.ancestry_compatible)),
        CleanRoomAnswer("Rooted subsystem?", bool(subsystem.subsystems), str(len(subsystem.subsystems))),
        CleanRoomAnswer("Positive signature depth?", subsystem.positive_signature_at_depth, str(subsystem.positive_signature_at_depth)),
        CleanRoomAnswer("Uniform constants?", t110.uniform_subsystem, t110.status),
        CleanRoomAnswer("Divergent constants rerouted?", all(c.outcome != "NONE" for c in constants), "checked"),
        CleanRoomAnswer("Oscillation geometric?", osc.geometric, osc.oscillation_class),
        CleanRoomAnswer("Oscillation implies reduction?", t111.no_persistent_oscillation, t111.reduction),
        CleanRoomAnswer("Omitted nodes controlled?", aug.no_discrete_gate_order, "augmented datum"),
        CleanRoomAnswer("T103 implies T089E?", t089e.status == "PROVED_LOCALLY" if t103.status == "PROVED_LOCALLY" else True, t089e.status),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    if t103.status == "PROVED_LOCALLY" and t109.status == "PROVED_LOCALLY" and t110.status == "PROVED_LOCALLY" and t111.status == "PROVED_LOCALLY":
        verdict: CleanRoomVerdict = "T103_CLEAN_ROOM_VERIFIED"
    elif passed >= 9:
        verdict = "T103_REPAIRABLE_GAP"
    else:
        verdict = "T103_INVALID"
    return T103CleanRoomAudit(verdict=verdict, answers=answers, messages=[f"passed={passed}, pigeonhole={mass.pigeonhole_route}"])


def diagnose_d057_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t103 = certify_t103_coherent(tree)
    t109 = certify_t109(tree)
    t110 = certify_t110(tree)
    t111 = certify_t111(tree)
    clean = audit_t103_clean_room(tree)
    if t103.status == "PROVED_LOCALLY" and clean.verdict == "T103_CLEAN_ROOM_VERIFIED":
        return "A"
    if t109.status == "PROVED_LOCALLY" and t110.status == "PROVED_LOCALLY" and t111.status != "PROVED_LOCALLY":
        return "B"
    if t111.status == "PROVED_LOCALLY" and t109.status != "PROVED_LOCALLY":
        return "C"
    if t103.status != "PROVED_LOCALLY" and t109.extraction == "ROUTE_OSCILLATION":
        return "D"
    return "E"
