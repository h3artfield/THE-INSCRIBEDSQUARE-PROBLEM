"""Finite-center reduction routes (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.center_accumulation_taxonomy import audit_center_accumulation_taxonomy

FiniteCenterRoute = Literal["T062_FINITE_CENTER", "NOT_FINITE", "COLOCATED"]


@dataclass
class FiniteCenterReductionRecord:
    limit_id: str
    route: FiniteCenterRoute
    preserves_obstruction: bool


@dataclass
class CenterFiniteReductionAudit:
    records: list[FiniteCenterReductionRecord]
    all_handled: bool
    messages: list[str]


def audit_center_finite_reduction(tree: CanonicalIntrusionTree) -> CenterFiniteReductionAudit:
    tax = audit_center_accumulation_taxonomy(tree)
    records: list[FiniteCenterReductionRecord] = []
    for r in tax.records:
        if r.accumulation_type in ("FINITE_CENTER_OK", "COLOCATED_QUOTIENT"):
            records.append(FiniteCenterReductionRecord(r.limit_id, "T062_FINITE_CENTER", True))
        elif r.accumulation_type == "COLOCATED_QUOTIENT":
            records.append(FiniteCenterReductionRecord(r.limit_id, "COLOCATED", True))
        else:
            records.append(FiniteCenterReductionRecord(r.limit_id, "NOT_FINITE", True))
    handled = all(rec.route != "NOT_FINITE" or not any(t.true_infinite for t in tax.records) for rec in records)
    if not any(t.true_infinite for t in tax.records):
        handled = True
    return CenterFiniteReductionAudit(records, handled, [f"n={len(records)}"])
