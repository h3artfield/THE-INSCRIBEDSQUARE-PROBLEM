"""Infinite-center accumulation taxonomy (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.infinite_center_limits import audit_infinite_center_limits

AccumulationType = Literal[
    "COUNTABLE_CENTER_TOWER",
    "UNCOUNTABLE_CENTER_DUST",
    "FINITE_CENTER_OK",
    "COLOCATED_QUOTIENT",
    "TRUE_INFINITE_CENTER",
]


@dataclass
class CenterAccumulationRecord:
    limit_id: str
    accumulation_type: AccumulationType
    true_infinite: bool


@dataclass
class CenterAccumulationTaxonomyAudit:
    records: list[CenterAccumulationRecord]
    exhaustive: bool
    messages: list[str]


def audit_center_accumulation_taxonomy(tree: CanonicalIntrusionTree) -> CenterAccumulationTaxonomyAudit:
    limits = audit_infinite_center_limits(tree)
    records: list[CenterAccumulationRecord] = []
    for r in limits.records:
        at: AccumulationType = "FINITE_CENTER_OK"
        true_inf = False
        if r.center_class == "COLOCATED_SINGLE_CENTER":
            at = "COLOCATED_QUOTIENT"
        elif r.center_class == "INFINITE_CENTER_ACCUMULATION":
            at = "TRUE_INFINITE_CENTER"
            true_inf = True
        elif r.center_class == "DIFFUSE_CENTER_CLOUD":
            at = "UNCOUNTABLE_CENTER_DUST"
            true_inf = True
        elif r.cover_number > 4:
            at = "COUNTABLE_CENTER_TOWER"
            true_inf = True
        records.append(CenterAccumulationRecord(r.limit_id, at, true_inf))
    return CenterAccumulationTaxonomyAudit(records, bool(records), [f"n={len(records)}"])
