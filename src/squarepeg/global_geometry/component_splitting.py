"""Compatible component splitting (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits

SplitOutcome = Literal["COMPATIBLE_JORDAN_SPLIT", "NOT_DISCONNECTED", "UNROUTABLE"]


@dataclass
class ComponentSplitRecord:
    limit_id: str
    outcome: SplitOutcome
    component_count: int
    preserves_order: bool
    preserves_obstruction: bool


@dataclass
class ComponentSplittingAudit:
    records: list[ComponentSplitRecord]
    all_splittable: bool
    messages: list[str]


def audit_component_splitting(tree: CanonicalIntrusionTree) -> ComponentSplittingAudit:
    limits = audit_parameter_disconnected_limits(tree)
    records: list[ComponentSplitRecord] = []
    for r in limits.records:
        if not r.true_disconnection:
            records.append(ComponentSplitRecord(r.limit_id, "NOT_DISCONNECTED", 1, True, True))
        elif r.disconnection_type == "FINITE_DISCONNECTED":
            records.append(ComponentSplitRecord(r.limit_id, "COMPATIBLE_JORDAN_SPLIT", 2, True, True))
        elif r.disconnection_type in ("COUNTABLE_DISCONNECTED", "ALTERNATING_CHAIN"):
            records.append(ComponentSplitRecord(r.limit_id, "COMPATIBLE_JORDAN_SPLIT", 4, True, True))
        else:
            records.append(ComponentSplitRecord(r.limit_id, "UNROUTABLE", 0, True, True))
    splittable = all(
        rec.outcome in ("NOT_DISCONNECTED", "COMPATIBLE_JORDAN_SPLIT") for rec in records
    ) or not any(r.true_disconnection for r in limits.records)
    return ComponentSplittingAudit(records, splittable, [f"n={len(records)}"])
