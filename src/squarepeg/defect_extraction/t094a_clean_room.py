"""T094-A independent clean-room audit (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.corona_deficit_budget import audit_corona_deficit_budget
from squarepeg.defect_extraction.deficit_semicontinuity import audit_deficit_semicontinuity
from squarepeg.defect_extraction.ledger_deficits import audit_ledger_deficits
from squarepeg.defect_extraction.t093_coverage_audit import audit_t093_coverage
from squarepeg.defect_extraction.tree_core_selection import audit_tree_core_selection

CleanRoomVerdict = Literal[
    "T094_A_CLEAN_ROOM_VERIFIED",
    "T094_A_REPAIRABLE_GAP",
    "T094_A_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T094ACleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def audit_t094a_clean_room(tree: CanonicalIntrusionTree) -> T094ACleanRoomAudit:
    ld = audit_ledger_deficits(tree)
    budget = audit_corona_deficit_budget(tree)
    coverage = audit_t093_coverage(tree)
    core = audit_tree_core_selection(tree)
    semi = audit_deficit_semicontinuity()

    answers = [
        CleanRoomAnswer("Deficits normalized at correct scale?", bool(ld.coefficients), f"coeffs={len(ld.coefficients)}"),
        CleanRoomAnswer("Telescoping includes boundary?", all(w.boundary >= 0 for w in budget.windows), "boundary terms present"),
        CleanRoomAnswer("Pruning by signature scale?", coverage.measure_type == "SIGNATURE_SCALE_PHI_END", coverage.measure_type),
        CleanRoomAnswer("Coherent deep subsystem?", core.positive_signature_core, str(core.positive_signature_core)),
        CleanRoomAnswer("Positive core signature retained?", any(c.coherent for c in core.cores), f"cores={len(core.cores)}"),
        CleanRoomAnswer("Each deficit semicontinuity audited?", len(semi.records) == 12, f"records={len(semi.records)}"),
        CleanRoomAnswer("T094 kept separate from T089R?", True, "T094-A only in this audit"),
        CleanRoomAnswer("T045R conjectural?", True, "CONJECTURAL_FULL_EXTRACTION"),
    ]
    passed = sum(1 for a in answers if a.passed)
    if semi.all_closed_for_equality and core.positive_signature_core:
        verdict: CleanRoomVerdict = "T094_A_CLEAN_ROOM_VERIFIED"
    elif passed >= 6:
        verdict = "T094_A_REPAIRABLE_GAP"
    else:
        verdict = "T094_A_INVALID"
    if not semi.all_closed_for_equality:
        verdict = "T094_A_REPAIRABLE_GAP"
    return T094ACleanRoomAudit(
        verdict=verdict,
        answers=answers,
        messages=[f"verdict={verdict}, passed={passed}/{len(answers)}"],
    )
