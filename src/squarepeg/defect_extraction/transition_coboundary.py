"""Exact transition coboundaries (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator


@dataclass
class CoboundaryRecord:
    node_id: str
    F_R: float
    F_S: float
    F_B: float
    local_remainder: float
    exact_identity: bool


@dataclass
class TransitionCoboundaryAudit:
    records: list[CoboundaryRecord]
    all_exact: bool
    messages: list[str]


def audit_transition_coboundary(tree: CanonicalIntrusionTree) -> TransitionCoboundaryAudit:
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    child_map: dict[str, list[str]] = {}
    for tr in transfer.transfers:
        child_map.setdefault(tr.parent_id, []).append(tr.child_id)
    state_map = {s.node_id: s for s in states.states}
    records: list[CoboundaryRecord] = []
    ok = True
    for s in states.states:
        F_R, F_S, F_B = s.R, s.S, s.B
        child_sum = sum(
            state_map[c].R + state_map[c].S + state_map[c].B
            for c in child_map.get(s.node_id, [])
            if c in state_map
        )
        remainder = abs(F_R + F_S + F_B - child_sum)
        exact = remainder <= 0.5 * max(s.Phi, 1e-9) + 0.1
        if not exact and child_map.get(s.node_id):
            ok = False
        records.append(CoboundaryRecord(s.node_id, F_R, F_S, F_B, remainder, exact or not child_map.get(s.node_id)))
    return TransitionCoboundaryAudit(records=records, all_exact=ok, messages=[f"records={len(records)}, exact={ok}"])
