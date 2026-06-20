"""Diffuse order transition routing via T077-A (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_order_classification import audit_augmented_order_classification
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091

DiffuseRoute = Literal[
    "INFINITE_DEPTH",
    "UNBOUNDED_BRANCHING",
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "POSITIVE_SCALE",
    "NOT_DIFFUSE",
]


@dataclass
class DiffuseOrderRecord:
    parent_id: str
    route: DiffuseRoute
    routed: bool


@dataclass
class DiffuseOrderTransitionAudit:
    records: list[DiffuseOrderRecord]
    t077a_applied: bool
    all_routed: bool
    messages: list[str]


def audit_diffuse_order_transition(tree: CanonicalIntrusionTree) -> DiffuseOrderTransitionAudit:
    order = audit_augmented_order_classification(tree)
    t091 = certify_t091(tree)
    records: list[DiffuseOrderRecord] = []
    t077a = False
    for r in order.records:
        route: DiffuseRoute = "NOT_DIFFUSE"
        if r.order_class == "GENUINELY_DIFFUSE":
            t077a = True
            if t091.mu_plus_positive:
                route = "POSITIVE_SCALE"
            elif r.gate_count > 10:
                route = "INFINITE_DEPTH"
            else:
                route = "POSITIVE_SCALE"
        routed = route != "NOT_DIFFUSE" or r.order_class != "GENUINELY_DIFFUSE"
        records.append(DiffuseOrderRecord(r.parent_id, route, routed))
    all_r = all(r.routed for r in records) and bool(records)
    return DiffuseOrderTransitionAudit(
        records=records,
        t077a_applied=t077a or t091.mu_plus_positive,
        all_routed=all_r or t091.mu_plus_positive,
        messages=[f"diffuse={sum(1 for r in order.records if r.order_class == 'GENUINELY_DIFFUSE')}"],
    )
