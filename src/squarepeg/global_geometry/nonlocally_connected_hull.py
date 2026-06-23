"""Nonlocally connected hull limits (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy

NLCRoute = Literal["INFINITE_CENTER_GEOMETRY", "PARAMETER_DISCONNECTED_LIMIT", "NOT_NLC"]


@dataclass
class NLCHullRecord:
    hull_id: str
    route: NLCRoute


@dataclass
class NonlocallyConnectedHullAudit:
    records: list[NLCHullRecord]
    all_routed: bool
    messages: list[str]


def audit_nonlocally_connected_hull(tree: CanonicalIntrusionTree) -> NonlocallyConnectedHullAudit:
    tax = audit_non_jordan_hull_taxonomy(tree)
    records: list[NLCHullRecord] = []
    for r in tax.records:
        if r.failure_type == "NONLOCALLY_CONNECTED_LIMIT":
            records.append(NLCHullRecord(r.hull_id, "INFINITE_CENTER_GEOMETRY"))
        else:
            records.append(NLCHullRecord(r.hull_id, "NOT_NLC"))
    return NonlocallyConnectedHullAudit(records, True, [f"n={len(records)}"])
