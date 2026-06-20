"""Gate-order marginal classification from Pi and Omega (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure

OrderClass = Literal[
    "ZERO_INVERSION",
    "FINITE_WIDTH",
    "COUNTABLE_SUMMABLE",
    "NONSUMMABLE_GRAPH",
    "GENUINELY_DIFFUSE",
]


@dataclass
class OrderClassRecord:
    parent_id: str
    order_class: OrderClass
    gate_count: int
    cross_area: float
    destination: str


@dataclass
class AugmentedOrderClassificationAudit:
    records: list[OrderClassRecord]
    all_routed: bool
    messages: list[str]


def _classify(gate_count: int, cross: float) -> tuple[OrderClass, str]:
    if cross < 1e-6:
        return "ZERO_INVERSION", "T068I"
    if gate_count <= 3:
        return "FINITE_WIDTH", "T073"
    if gate_count <= 8 and cross < 0.5:
        return "COUNTABLE_SUMMABLE", "T073I"
    if cross < 1.0:
        return "NONSUMMABLE_GRAPH", "T076"
    return "GENUINELY_DIFFUSE", "T077-A"


def audit_augmented_order_classification(tree: CanonicalIntrusionTree) -> AugmentedOrderClassificationAudit:
    pi = audit_marked_gate_measure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    omap = {m.parent_id: m for m in omega.measures}
    records: list[OrderClassRecord] = []
    for m in pi.measures:
        gc = len(m.atoms)
        cross = omap[m.parent_id].cross_area if m.parent_id in omap else 0.0
        oc, dest = _classify(gc, cross)
        records.append(OrderClassRecord(m.parent_id, oc, gc, cross, dest))
    all_r = bool(records)
    return AugmentedOrderClassificationAudit(records=records, all_routed=all_r, messages=[f"n={len(records)}"])
