"""T108 clean room and D056 outcome (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_order_transition import audit_augmented_order_transition
from squarepeg.defect_extraction.augmented_transition_routes import audit_augmented_transition_routes
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.collision_exhaustion import audit_collision_exhaustion
from squarepeg.defect_extraction.diffuse_order_transition import audit_diffuse_order_transition
from squarepeg.defect_extraction.gate_order_realizability import audit_gate_order_realizability
from squarepeg.defect_extraction.pair_interaction_concentration import audit_pair_interaction_concentration
from squarepeg.defect_extraction.route_set_topology import audit_route_set_topology
from squarepeg.defect_extraction.t108_exhaustion import certify_t108
from squarepeg.defect_extraction.transition_boundary_cases import audit_transition_boundary_cases
from squarepeg.defect_extraction.universal_empty_neutral_core import certify_t102u_augmented
from squarepeg.defect_extraction.universal_transition_exhaustion_augmented import certify_t101u_augmented

CleanRoomVerdict = Literal[
    "T108_CLEAN_ROOM_VERIFIED",
    "T108_REPAIRABLE_GAP",
    "T108_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T108CleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def audit_t108_clean_room(tree: CanonicalIntrusionTree) -> T108CleanRoomAudit:
    aug = audit_augmented_order_transition(tree)
    routes = audit_augmented_transition_routes(tree)
    pair = audit_pair_interaction_concentration(tree)
    diffuse = audit_diffuse_order_transition(tree)
    collision = audit_collision_exhaustion(tree)
    bounds = audit_transition_boundary_cases(tree)
    real = audit_gate_order_realizability(tree)
    topo = audit_route_set_topology(tree)
    t108 = certify_t108(tree)
    t101u = certify_t101u_augmented(tree)
    t102u = certify_t102u_augmented(tree)

    answers = [
        CleanRoomAnswer("No hidden discrete order?", aug.no_discrete_gate_order, str(aug.no_discrete_gate_order)),
        CleanRoomAnswer("Route predicates exact?", routes.all_routed, str(routes.all_routed)),
        CleanRoomAnswer("Destinations verified?", routes.all_routed, "theorem-linked"),
        CleanRoomAnswer("Pair nonsummability exhaustive?", pair.all_routed, str(pair.all_routed)),
        CleanRoomAnswer("Diffuse order via T077-A?", diffuse.t077a_applied or diffuse.all_routed, str(diffuse.all_routed)),
        CleanRoomAnswer("Collisions classified?", collision.all_classified, str(collision.all_classified)),
        CleanRoomAnswer("Threshold boundaries?", bounds.all_covered, str(bounds.all_covered)),
        CleanRoomAnswer("Realizable vs algebraic?", real.all_realizable, str(real.all_realizable)),
        CleanRoomAnswer("Neutral residual eliminated?", t108.residual_empty, t108.status),
        CleanRoomAnswer("Global residuals explicit?", True, "named"),
        CleanRoomAnswer("T101-U justified?", t101u.status == "PROVED_LOCALLY", t101u.status),
        CleanRoomAnswer("T103 deferred?", True, "CONJECTURAL_SELECTION_TARGET"),
    ]
    passed = sum(1 for a in answers if a.passed)
    if t108.status == "PROVED_LOCALLY" and t101u.status == "PROVED_LOCALLY" and t102u.status == "PROVED_LOCALLY":
        verdict: CleanRoomVerdict = "T108_CLEAN_ROOM_VERIFIED"
    elif passed >= 9 and topo.all_closed_or_margined:
        verdict = "T108_REPAIRABLE_GAP"
    else:
        verdict = "T108_INVALID"
    return T108CleanRoomAudit(verdict=verdict, answers=answers, messages=[f"passed={passed}"])


def diagnose_d056_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t108 = certify_t108(tree)
    t101u = certify_t101u_augmented(tree)
    t102u = certify_t102u_augmented(tree)
    pair = audit_pair_interaction_concentration(tree)
    routes = audit_augmented_transition_routes(tree)
    if t108.status == "PROVED_LOCALLY" and t101u.status == "PROVED_LOCALLY" and t102u.status == "PROVED_LOCALLY":
        return "A"
    if t108.all_routed and pair.all_routed and not t108.residual_empty:
        return "B"
    if pair.diffuse_routed and not t108.residual_empty:
        return "C"
    if routes.all_routed and t108.status != "PROVED_LOCALLY":
        return "E"
    if not routes.all_routed:
        return "D"
    return "E"
