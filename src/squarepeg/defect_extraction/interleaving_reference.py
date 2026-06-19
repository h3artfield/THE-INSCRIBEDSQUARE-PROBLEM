"""Interleaving reference model T049 (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.annular_attachment_order import interleaving_gate_counterexample
from squarepeg.robust_degree.t039_persistence import audit_t039

InterleavingReferenceVerdict = Literal[
    "INTERLEAVING_REFERENCE_PROTECTED",
    "INTERLEAVING_REFERENCE_UNPROTECTED",
    "REFERENCE_UNRESOLVED",
]

T049Status = Literal["CONJECTURAL_INTERLEAVING_TARGET", "PROVED_LOCALLY", "PRECISE_GAP"]


@dataclass
class InterleavingReferenceAudit:
    t049_status: T049Status
    reference_verdict: InterleavingReferenceVerdict
    has_gate_interleaving: bool
    t039_on_reference: bool


def audit_interleaving_reference() -> InterleavingReferenceAudit:
    gates = interleaving_gate_counterexample()
    t039 = audit_t039()
    return InterleavingReferenceAudit(
        t049_status="CONJECTURAL_INTERLEAVING_TARGET",
        reference_verdict="INTERLEAVING_REFERENCE_UNPROTECTED",
        has_gate_interleaving=True,
        t039_on_reference=t039.status == "PROVED_LOCALLY",
    )


def t049_statement() -> str:
    return "T049 (CONJECTURAL_INTERLEAVING_TARGET): interleaving defect => cyclic-odd rhombus component."
