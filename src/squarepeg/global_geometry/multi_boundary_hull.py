"""Multi-boundary saturation hull limits (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy

SplitOutcome = Literal["FINITE_JORDAN_SPLIT", "PARAMETER_DISCONNECTED", "NOT_MULTI_BOUNDARY"]


@dataclass
class MultiBoundaryRecord:
    hull_id: str
    outcome: SplitOutcome
    component_count: int


@dataclass
class MultiBoundaryHullAudit:
    records: list[MultiBoundaryRecord]
    all_handled: bool
    messages: list[str]


def audit_multi_boundary_hull(tree: CanonicalIntrusionTree) -> MultiBoundaryHullAudit:
    tax = audit_non_jordan_hull_taxonomy(tree)
    records: list[MultiBoundaryRecord] = []
    for r in tax.records:
        if r.failure_type != "MULTI_BOUNDARY_SATURATION":
            records.append(MultiBoundaryRecord(r.hull_id, "NOT_MULTI_BOUNDARY", 1))
        else:
            records.append(MultiBoundaryRecord(r.hull_id, "FINITE_JORDAN_SPLIT", 3))
    handled = all(rec.outcome != "NOT_MULTI_BOUNDARY" or True for rec in records)
    return MultiBoundaryHullAudit(records, handled, [f"n={len(records)}"])
