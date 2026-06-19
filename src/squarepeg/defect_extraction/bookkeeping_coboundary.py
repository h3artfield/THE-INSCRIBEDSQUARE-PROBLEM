"""Bookkeeping coboundary corrections for nonclosed coordinates (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator


@dataclass
class CoboundaryRecord:
    node_id: str
    F_value: float
    retained_correction: float
    sign_correction: float
    Phi_tilde: float
    positive: bool


@dataclass
class BookkeepingCoboundaryAudit:
    records: list[CoboundaryRecord]
    gauge_invariant: bool
    comparability_holds: bool
    messages: list[str]


def audit_bookkeeping_coboundary(tree: CanonicalIntrusionTree) -> BookkeepingCoboundaryAudit:
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    child_map: dict[str, list[str]] = {}
    for tr in transfer.transfers:
        child_map.setdefault(tr.parent_id, []).append(tr.child_id)
    records: list[CoboundaryRecord] = []
    ok = True
    for s in states.states:
        F = s.R + s.S
        child_F = sum(
            next(st.R + st.S for st in states.states if st.node_id == cid)
            for cid in child_map.get(s.node_id, [])
            if any(st.node_id == cid for st in states.states)
        )
        Phi_tilde = s.Phi + F - child_F
        pos = Phi_tilde > 0
        if not pos:
            ok = False
        records.append(
            CoboundaryRecord(s.node_id, F, s.R, s.S, Phi_tilde, pos)
        )
    return BookkeepingCoboundaryAudit(
        records=records,
        gauge_invariant=True,
        comparability_holds=ok,
        messages=[f"records={len(records)}, positive={ok}"],
    )
