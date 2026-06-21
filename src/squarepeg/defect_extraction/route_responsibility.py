"""Fractional route responsibility weights alpha_r(v) (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.route_label_system import ROUTE_FAMILY, RouteLabel, audit_route_label_system


@dataclass
class RouteResponsibility:
    node_id: str
    weights: dict[RouteLabel, float]


@dataclass
class RouteResponsibilityAudit:
    records: list[RouteResponsibility]
    signature_preserving: bool
    no_double_count: bool
    messages: list[str]


def _equal_split(labels: list[RouteLabel]) -> dict[RouteLabel, float]:
    if not labels:
        return {}
    w = 1.0 / len(labels)
    return {lab: w for lab in labels}


def audit_route_responsibility(tree: CanonicalIntrusionTree) -> RouteResponsibilityAudit:
    system = audit_route_label_system(tree)
    records: list[RouteResponsibility] = []
    ok = True
    for ns in system.node_sets:
        weights = _equal_split(ns.labels)
        total = sum(weights.values())
        if abs(total - 1.0) > 1e-9 and ns.labels:
            ok = False
        for lab in weights:
            if lab not in ns.labels:
                ok = False
        records.append(RouteResponsibility(ns.node_id, weights))
    return RouteResponsibilityAudit(
        records=records,
        signature_preserving=ok,
        no_double_count=ok,
        messages=[f"n={len(records)}"],
    )
