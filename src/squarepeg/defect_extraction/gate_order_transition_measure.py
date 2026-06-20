"""Gate-order transition measures (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree


@dataclass
class GateOrderRecord:
    node_id: str
    gate_count: int
    inversion_energy: float
    monotone_width: float
    block_count: int


@dataclass
class GateOrderTransitionAudit:
    records: list[GateOrderRecord]
    unbounded_complexity: bool
    messages: list[str]


def audit_gate_order_transition_measure(tree: CanonicalIntrusionTree) -> GateOrderTransitionAudit:
    states = audit_augmented_neutral_state(tree)
    records: list[GateOrderRecord] = []
    unbounded = False
    for s in states.states:
        node = tree.nodes.get(s.node_id)
        if not node:
            continue
        gc = node.gate_count
        inv = s.G / max(s.Phi, 1e-12)
        width = node.diameter * gc
        blocks = max(1, gc // 2)
        if gc > 6 or inv > 5.0:
            unbounded = True
        records.append(GateOrderRecord(s.node_id, gc, inv, width, blocks))
    return GateOrderTransitionAudit(
        records=records,
        unbounded_complexity=unbounded,
        messages=[f"records={len(records)}, unbounded={unbounded}"],
    )
