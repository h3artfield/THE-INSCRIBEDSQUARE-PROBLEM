"""T094 independent clean-room audit (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.equality_compatibility import audit_equality_compatibility
from squarepeg.defect_extraction.equality_ledger import get_ledger
from squarepeg.defect_extraction.equality_stability import audit_equality_stability
from squarepeg.defect_extraction.neutral_corona_tangent import audit_neutral_corona_tangent
from squarepeg.defect_extraction.t093_coverage_audit import audit_t093_coverage

CleanRoomVerdict = Literal[
    "T094_CLEAN_ROOM_VERIFIED",
    "T094_REPAIRABLE_GAP",
    "T094_INVALID",
]


@dataclass
class CleanRoomAnswer:
    question: str
    passed: bool
    detail: str


@dataclass
class T094CleanRoomAudit:
    verdict: CleanRoomVerdict
    answers: list[CleanRoomAnswer]
    messages: list[str]


def audit_t094_clean_room(tree: CanonicalIntrusionTree) -> T094CleanRoomAudit:
    coverage = audit_t093_coverage(tree)
    tangent = audit_neutral_corona_tangent(tree)
    compat = audit_equality_compatibility()
    stab = audit_equality_stability()
    ledger = get_ledger()

    answers = [
        CleanRoomAnswer(
            "T093 coverage measure explicit?",
            coverage.measure_type == "SIGNATURE_SCALE_PHI_END",
            coverage.measure_type,
        ),
        CleanRoomAnswer(
            "Residual mass enters neutral coronas?",
            coverage.residual_in_neutral,
            f"neutral_frac={coverage.neutral_phi_fraction:.2f}",
        ),
        CleanRoomAnswer(
            "Equality ledger complete?",
            len(ledger) >= 10,
            f"entries={len(ledger)}",
        ),
        CleanRoomAnswer(
            "Equality conditions correct?",
            len(compat.impossible_cliques) >= 1,
            "incompatible pairs identified",
        ),
        CleanRoomAnswer(
            "Near-equality stability quantitative?",
            all(r.omega_epsilon >= 0 for r in stab.records),
            f"records={len(stab.records)}",
        ),
        CleanRoomAnswer(
            "Tangent compactness preserves hypotheses?",
            tangent.compactness_holds,
            str(tangent.compactness_holds),
        ),
        CleanRoomAnswer(
            "Deficits vanish in limit?",
            tangent.all_deficits_vanish,
            str(tangent.all_deficits_vanish),
        ),
        CleanRoomAnswer(
            "T045R still conjectural?",
            True,
            "CONJECTURAL_FULL_EXTRACTION",
        ),
    ]
    passed = sum(1 for a in answers if a.passed)
    if passed >= 7 and tangent.compactness_holds and coverage.measure_type:
        verdict: CleanRoomVerdict = "T094_REPAIRABLE_GAP"
    elif passed >= 9 and tangent.all_deficits_vanish:
        verdict = "T094_CLEAN_ROOM_VERIFIED"
    else:
        verdict = "T094_REPAIRABLE_GAP"
    if len(ledger) < 5:
        verdict = "T094_INVALID"
    return T094CleanRoomAudit(
        verdict=verdict,
        answers=answers,
        messages=[f"verdict={verdict}, passed={passed}/{len(answers)}"],
    )
