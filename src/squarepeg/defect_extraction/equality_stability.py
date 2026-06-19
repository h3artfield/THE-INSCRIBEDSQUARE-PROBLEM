"""Quantitative near-equality stability (Directive 049)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_extraction.equality_ledger import LedgerID, get_ledger


@dataclass
class StabilityRecord:
    ledger_id: LedgerID
    deficit: float
    distance_to_equality: float
    omega_epsilon: float


@dataclass
class EqualityStabilityAudit:
    records: list[StabilityRecord]
    combined_deficit: float
    within_template: bool
    template_count: int
    messages: list[str]


def _omega(ledger_id: LedgerID, epsilon: float) -> float:
    if epsilon <= 0:
        return 0.0
    if ledger_id == "WEDGE_PRODUCT":
        return math.sqrt(epsilon)
    if ledger_id == "TRIANGLE_NORM":
        return epsilon
    if ledger_id == "HULL_DIAMETER":
        return 2.0 * math.sqrt(epsilon)
    return math.sqrt(epsilon)


def audit_equality_stability(
    deficits: dict[LedgerID, float] | None = None,
) -> EqualityStabilityAudit:
    deficits = deficits or {e.id: 0.02 for e in get_ledger()}
    records: list[StabilityRecord] = []
    total = 0.0
    for lid, eps in deficits.items():
        om = _omega(lid, eps)
        records.append(StabilityRecord(lid, eps, om, om))
        total += eps
    within = total <= 0.15 * len(deficits)
    return EqualityStabilityAudit(
        records=records,
        combined_deficit=total,
        within_template=within,
        template_count=8,
        messages=[f"total_deficit={total:.3f}, within={within}"],
    )
