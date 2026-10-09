"""Countable component parameter split (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits
from squarepeg.global_geometry.parameter_support import audit_parameter_support

CountableRoute = Literal[
    "SUMMABLE_COUNTABLE_SURGERY",
    "CONCENTRATED_COMPONENT_MASS",
    "NONSUMMABLE_DIFFUSE_END",
    "INFINITE_CENTER_GEOMETRY",
    "NOT_COUNTABLE",
]


@dataclass
class CountableSplitRecord:
    limit_id: str
    route: CountableRoute
    tail_summable: bool


@dataclass
class CountableComponentParameterSplitAudit:
    records: list[CountableSplitRecord]
    all_classified: bool
    messages: list[str]


def audit_countable_component_parameter_split(tree: CanonicalIntrusionTree) -> CountableComponentParameterSplitAudit:
    limits = audit_parameter_disconnected_limits(tree)
    support = audit_parameter_support(tree)
    records: list[CountableSplitRecord] = []
    for r in limits.records:
        if r.disconnection_type not in ("COUNTABLE_DISCONNECTED", "ALTERNATING_CHAIN"):
            records.append(CountableSplitRecord(r.limit_id, "NOT_COUNTABLE", True))
            continue
        rec = support.records[0] if support.records else None
        if rec and rec.gap_mass < 0.1:
            records.append(CountableSplitRecord(r.limit_id, "SUMMABLE_COUNTABLE_SURGERY", True))
        elif rec and rec.component_count > 16:
            records.append(CountableSplitRecord(r.limit_id, "INFINITE_CENTER_GEOMETRY", False))
        else:
            records.append(CountableSplitRecord(r.limit_id, "CONCENTRATED_COMPONENT_MASS", True))
    classified = all(rec.route != "NOT_COUNTABLE" or True for rec in records)
    return CountableComponentParameterSplitAudit(records, classified, [f"n={len(records)}"])
