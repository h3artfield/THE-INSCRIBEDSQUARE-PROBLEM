"""Gate-order realizability classification (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_order_transition import audit_augmented_order_transition
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_measure_weak_closure import audit_gate_measure_weak_closure

Realizability = Literal[
    "FINITE_REALIZABLE",
    "COUNTABLE_REALIZABLE",
    "MEASURE_REALIZABLE",
    "LIMIT_REALIZABLE",
    "ALGEBRAIC_ONLY",
]


@dataclass
class RealizabilityRecord:
    parent_id: str
    class_: Realizability


@dataclass
class GateOrderRealizabilityAudit:
    records: list[RealizabilityRecord]
    all_realizable: bool
    messages: list[str]


def audit_gate_order_realizability(tree: CanonicalIntrusionTree) -> GateOrderRealizabilityAudit:
    aug = audit_augmented_order_transition(tree)
    closure = audit_gate_measure_weak_closure(tree)
    records: list[RealizabilityRecord] = []
    for t in aug.transitions:
        rc: Realizability = "FINITE_REALIZABLE" if closure.discrete_gate_order_eliminated else "ALGEBRAIC_ONLY"
        records.append(RealizabilityRecord(t.parent_id, rc))
    all_r = all(r.class_ != "ALGEBRAIC_ONLY" for r in records) and bool(records)
    return GateOrderRealizabilityAudit(records=records, all_realizable=all_r, messages=[f"n={len(records)}"])
