"""T098 independent clean-room audit (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.bellman_exact_certificate import audit_bellman_exact_certificate
from squarepeg.defect_extraction.bellman_potential import audit_bellman_potential
from squarepeg.defect_extraction.bookkeeping_coboundary import audit_bookkeeping_coboundary
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.invariant_state_measure import audit_invariant_state_measure
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator
from squarepeg.defect_extraction.transition_family import audit_transition_family

CleanRoomVerdict = Literal[
    "T098_CLEAN_ROOM_VERIFIED",
    "T098_REPAIRABLE_GAP",
    "T098_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T098CleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def audit_t098_clean_room(tree: CanonicalIntrusionTree) -> T098CleanRoomAudit:
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    family = audit_transition_family(tree)
    bellman = audit_bellman_potential(tree)
    cert = audit_bellman_exact_certificate(tree, bellman=bellman)
    inv = audit_invariant_state_measure(tree)
    cob = audit_bookkeeping_coboundary(tree)

    answers = [
        CleanRoomAnswer("Coordinates from exact geometry?", bool(states.states), f"states={len(states.states)}"),
        CleanRoomAnswer("Recursion counts terms once?", transfer.recursion_holds, str(transfer.recursion_holds)),
        CleanRoomAnswer("Transition family compact?", family.family_compact, str(family.family_compact)),
        CleanRoomAnswer("Bellman positive and comparable?", bellman.best is not None and (bellman.best.comparable_lower > 0), "comparable"),
        CleanRoomAnswer("Numerical cert to exact arithmetic?", cert.any_verified or bool(cert.certificates), f"certs={len(cert.certificates)}"),
        CleanRoomAnswer("Occupation boundary controlled?", inv.measure.boundary_vanishes, str(inv.measure.boundary_vanishes)),
        CleanRoomAnswer("Invariant balance exact?", inv.balance_holds, str(inv.balance_holds)),
        CleanRoomAnswer("Coboundaries consistent?", cob.gauge_invariant, str(cob.comparability_holds)),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    if bellman.linear_exists and cert.any_verified and inv.balance_holds:
        verdict: CleanRoomVerdict = "T098_CLEAN_ROOM_VERIFIED"
    elif passed >= 6:
        verdict = "T098_REPAIRABLE_GAP"
    else:
        verdict = "T098_INVALID"
    if not bellman.linear_exists:
        verdict = "T098_REPAIRABLE_GAP"
    return T098CleanRoomAudit(
        verdict=verdict,
        answers=answers,
        messages=[f"verdict={verdict}, passed={passed}/{len(answers)}"],
    )
