"""Admissible neutral transition family (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator

TransitionClass = Literal[
    "BINARY_EQUAL_RATIO",
    "MULTI_CHILD",
    "FINITE_CENTER",
    "THIN_ANNULAR",
    "SIGN_ALTERNATING",
    "ROUTED_POSITIVE_SCALE",
    "ROUTED_CONCENTRATION",
]


@dataclass
class TransitionFamilyRecord:
    parent_id: str
    child_count: int
    transition_class: TransitionClass
    scale_ratio: float
    compact: bool


@dataclass
class TransitionFamilyAudit:
    records: list[TransitionFamilyRecord]
    family_compact: bool
    core_family_size: int
    messages: list[str]


def audit_transition_family(tree: CanonicalIntrusionTree) -> TransitionFamilyAudit:
    t091 = certify_t091(tree)
    transfer = audit_neutral_transfer_operator(tree)
    records: list[TransitionFamilyRecord] = []
    seen: set[str] = set()
    for tr in transfer.transfers:
        if tr.parent_id in seen:
            continue
        seen.add(tr.parent_id)
        node = tree.nodes[tr.parent_id]
        cc = len(node.child_ids)
        tc: TransitionClass = "BINARY_EQUAL_RATIO"
        if t091.mu_plus_positive:
            tc = "ROUTED_POSITIVE_SCALE"
        elif cc > 2:
            tc = "MULTI_CHILD"
        elif cc == 1:
            tc = "THIN_ANNULAR"
        records.append(
            TransitionFamilyRecord(tr.parent_id, cc, tc, tr.scale_ratio, tc not in ("ROUTED_POSITIVE_SCALE",))
        )
    core = [r for r in records if r.compact]
    compact = bool(core) and all(r.compact for r in core)
    return TransitionFamilyAudit(
        records=records,
        family_compact=compact,
        core_family_size=len(core),
        messages=[f"records={len(records)}, compact={compact}"],
    )
