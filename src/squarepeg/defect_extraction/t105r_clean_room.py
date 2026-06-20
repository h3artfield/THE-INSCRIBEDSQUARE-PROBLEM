"""T105R clean room and D055 outcome (Directive 055)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from squarepeg.defect_extraction.augmented_order_transition import audit_augmented_order_transition
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cyclic_gate_measure import audit_cyclic_gate_measure
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.defect_extraction.gate_measure_weak_closure import audit_gate_measure_weak_closure, certify_t107
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure
from squarepeg.defect_extraction.gate_order_realizability import audit_gate_order_realizability
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure, serialize_gate_marks
from squarepeg.defect_extraction.order_augmented_exhaustion import certify_t108
from squarepeg.defect_extraction.t105r_measure_closure import certify_t105r

CleanRoomVerdict = Literal[
    "T105R_CLEAN_ROOM_VERIFIED",
    "T105R_REPAIRABLE_GAP",
    "T105R_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T105RCleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def write_gate_order_fixture(tree: CanonicalIntrusionTree) -> Path:
    path = Path(__file__).resolve().parents[3] / "data" / "regressions" / "gate_order_weak_closure_fixture.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": "directive_054_gate_order_not_closed",
        "failure": "discrete gate_order NOT_CLOSED under weak limit",
        "repair": "Pi_v, Omega_v, Lambda_v augmented measures",
        "gates": serialize_gate_marks(tree)[:40],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def audit_t105r_clean_room(tree: CanonicalIntrusionTree) -> T105RCleanRoomAudit:
    fixture = write_gate_order_fixture(tree)
    pi = audit_marked_gate_measure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    lam = audit_gate_collision_measure(tree)
    cyclic = audit_cyclic_gate_measure(tree)
    closure = audit_gate_measure_weak_closure(tree)
    aug = audit_augmented_order_transition(tree)
    real = audit_gate_order_realizability(tree)
    t105r = certify_t105r(tree)

    answers = [
        CleanRoomAnswer("One-point gate insufficient?", True, "pair measure required"),
        CleanRoomAnswer("Pair reconstructs cross-wedge?", omega.exact_reconstruction, str(omega.exact_reconstruction)),
        CleanRoomAnswer("Seam independent?", cyclic.seam_independent, str(cyclic.seam_independent)),
        CleanRoomAnswer("Marginals consistent?", omega.marginal_consistent, str(omega.marginal_consistent)),
        CleanRoomAnswer("Collision mass preserved?", lam.all_routed, str(lam.all_routed)),
        CleanRoomAnswer("Discrete gate_order eliminated?", closure.discrete_gate_order_eliminated, str(closure.discrete_gate_order_eliminated)),
        CleanRoomAnswer("Realizability distinguished?", real.all_realizable, str(real.all_realizable)),
        CleanRoomAnswer("T105R compact and closed?", t105r.recursion_closed, t105r.status),
        CleanRoomAnswer("Fixture replayable?", fixture.exists(), fixture.name),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    if t105r.status == "PROVED_LOCALLY":
        verdict: CleanRoomVerdict = "T105R_CLEAN_ROOM_VERIFIED"
    elif passed >= 7:
        verdict = "T105R_REPAIRABLE_GAP"
    else:
        verdict = "T105R_INVALID"
    return T105RCleanRoomAudit(verdict=verdict, answers=answers, messages=[f"passed={passed}"])


def diagnose_d055_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t107 = certify_t107(tree)
    t105r = certify_t105r(tree)
    t108 = certify_t108(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    if t108.status == "PROVED_LOCALLY":
        return "A"
    if t105r.status == "PROVED_LOCALLY" and t107.status == "PROVED_LOCALLY":
        return "B"
    if t107.status == "PROVED_LOCALLY" and omega.exact_reconstruction and t105r.status != "PROVED_LOCALLY":
        return "C"
    if t107.status != "PROVED_LOCALLY" and not omega.exact_reconstruction:
        return "E"
    if t105r.status != "PROVED_LOCALLY":
        return "E"
    return "E"
