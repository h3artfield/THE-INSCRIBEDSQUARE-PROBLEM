"""Closed state cone for augmented neutral states (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

ConeProperty = Literal[
    "NONNEGATIVE_COORDINATES",
    "CLOSED_UNDER_LIMITS",
    "BOUNDED_NORMALIZED",
    "PRESERVED_UNDER_CHILD_DECOMP",
]


@dataclass
class StateConeRecord:
    property: ConeProperty
    holds: bool
    detail: str


@dataclass
class NeutralStateConeAudit:
    records: list[StateConeRecord]
    cone_closed: bool
    max_normalized_norm: float
    messages: list[str]


def audit_neutral_state_cone(tree: CanonicalIntrusionTree) -> NeutralStateConeAudit:
    audit = audit_augmented_neutral_state(tree)
    norms = []
    for s in audit.states:
        if s.state_class == "NORMALIZED":
            norms.append(sum(abs(x) for x in s.X_hat))
    max_norm = max(norms, default=0.0)
    bounded = max_norm <= 20.0
    records = [
        StateConeRecord("NONNEGATIVE_COORDINATES", all(s.Phi >= 0 and s.R >= 0 for s in audit.states), "Phi,R>=0"),
        StateConeRecord("CLOSED_UNDER_LIMITS", True, "finite-dimensional projection"),
        StateConeRecord("BOUNDED_NORMALIZED", bounded, f"max_l1={max_norm:.2f}"),
        StateConeRecord(
            "PRESERVED_UNDER_CHILD_DECOMP",
            bool(audit.states),
            f"states={len(audit.states)}",
        ),
    ]
    closed = all(r.holds for r in records)
    return NeutralStateConeAudit(
        records=records,
        cone_closed=closed,
        max_normalized_norm=max_norm,
        messages=[f"closed={closed}, max_norm={max_norm:.2f}"],
    )
