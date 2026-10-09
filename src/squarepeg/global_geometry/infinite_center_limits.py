"""Curve-level infinite-center limit geometry (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.infinite_center_end_geometry import audit_infinite_center_end_geometry

CenterClass = Literal[
    "FINITE_CENTER",
    "INFINITE_CENTER_ACCUMULATION",
    "DIFFUSE_CENTER_CLOUD",
    "COLOCATED_SINGLE_CENTER",
    "NOT_APPLICABLE",
]


@dataclass
class InfiniteCenterLimitRecord:
    limit_id: str
    center_class: CenterClass
    cover_number: int
    curve_level: bool


@dataclass
class InfiniteCenterLimitAudit:
    records: list[InfiniteCenterLimitRecord]
    curve_level: bool
    infinite_center: bool
    messages: list[str]


def audit_infinite_center_limits(tree: CanonicalIntrusionTree) -> InfiniteCenterLimitAudit:
    ic = audit_infinite_center_end_geometry(tree)
    centers = {n.center for n in tree.nodes.values()}
    colocated = len(centers) == 1
    cc: CenterClass = "NOT_APPLICABLE"
    if colocated and not ic.infinite_center:
        cc = "COLOCATED_SINGLE_CENTER"
    elif ic.infinite_center and ic.diffuse_end_measure:
        cc = "DIFFUSE_CENTER_CLOUD"
    elif ic.infinite_center:
        cc = "INFINITE_CENTER_ACCUMULATION"
    else:
        cc = "FINITE_CENTER"
    max_nc = max((r.N_c for r in ic.records), default=1)
    records = [InfiniteCenterLimitRecord("primary", cc, max_nc, True)]
    return InfiniteCenterLimitAudit(records, True, ic.infinite_center, ic.messages)
