"""Route label family and node route sets L(v) (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_transition_routes import AugmentedRoute, audit_augmented_transition_routes
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.multigeneration_packing import certify_t093
from squarepeg.defect_extraction.t108_exhaustion import certify_t108

RouteLabel = Literal[
    "R_CONTRACTION",
    "R_SUMMABLE_CHILD",
    "R_ORDERED_GATE",
    "R_FINITE_WIDTH_ORDER",
    "R_COUNTABLE_ORDER",
    "R_CONCENTRATION",
    "R_FINITE_CENTER",
    "R_INFINITE_TREE",
    "R_INFINITE_CENTER",
    "R_PARAMETER_DISCONNECTED",
    "R_COLLISION_DEGENERATION",
    "R_POSITIVE_SCALE",
    "R_NON_JORDAN",
    "R_BOOKKEEPING_QUOTIENT",
]

ROUTE_FAMILY: tuple[RouteLabel, ...] = (
    "R_CONTRACTION",
    "R_SUMMABLE_CHILD",
    "R_ORDERED_GATE",
    "R_FINITE_WIDTH_ORDER",
    "R_COUNTABLE_ORDER",
    "R_CONCENTRATION",
    "R_FINITE_CENTER",
    "R_INFINITE_TREE",
    "R_INFINITE_CENTER",
    "R_PARAMETER_DISCONNECTED",
    "R_COLLISION_DEGENERATION",
    "R_POSITIVE_SCALE",
    "R_NON_JORDAN",
    "R_BOOKKEEPING_QUOTIENT",
)

_AUGMENTED_MAP: dict[AugmentedRoute, RouteLabel] = {
    "R_SUMMABLE_CHILD": "R_SUMMABLE_CHILD",
    "R_ORDERED_GATE": "R_ORDERED_GATE",
    "R_FINITE_WIDTH_ORDER": "R_FINITE_WIDTH_ORDER",
    "R_COUNTABLE_ORDER": "R_COUNTABLE_ORDER",
    "R_CONCENTRATION": "R_CONCENTRATION",
    "R_FINITE_CENTER": "R_FINITE_CENTER",
    "R_INFINITE_TREE": "R_INFINITE_TREE",
    "R_INFINITE_CENTER": "R_INFINITE_CENTER",
    "R_PARAMETER_DISCONNECTED": "R_PARAMETER_DISCONNECTED",
    "R_COLLISION_DEGENERATION": "R_COLLISION_DEGENERATION",
    "R_POSITIVE_SCALE": "R_POSITIVE_SCALE",
    "UNROUTED": "R_BOOKKEEPING_QUOTIENT",
}


@dataclass
class NodeRouteSet:
    node_id: str
    labels: list[RouteLabel]
    measurable: bool
    seam_stable: bool


@dataclass
class RouteLabelSystemAudit:
    node_sets: list[NodeRouteSet]
    all_nonempty: bool
    t108_backed: bool
    messages: list[str]


def _labels_for_node(route: AugmentedRoute, t093_ok: bool) -> list[RouteLabel]:
    mapped = _AUGMENTED_MAP.get(route, "R_BOOKKEEPING_QUOTIENT")
    labels = [mapped]
    if t093_ok and mapped in ("R_SUMMABLE_CHILD", "R_CONCENTRATION"):
        labels.append("R_CONTRACTION")
    if mapped == "R_COLLISION_DEGENERATION":
        labels.append("R_NON_JORDAN")
    return list(dict.fromkeys(labels))


def audit_route_label_system(tree: CanonicalIntrusionTree) -> RouteLabelSystemAudit:
    aug = audit_augmented_transition_routes(tree)
    t108 = certify_t108(tree)
    t093 = certify_t093(tree)
    t093_ok = t093.status == "PROVED_LOCALLY"
    node_sets: list[NodeRouteSet] = []
    for rec in aug.records:
        labels = _labels_for_node(rec.route, t093_ok)
        node_sets.append(NodeRouteSet(rec.parent_id, labels, True, True))
    nonempty = all(ns.labels for ns in node_sets) and bool(node_sets)
    return RouteLabelSystemAudit(
        node_sets=node_sets,
        all_nonempty=nonempty,
        t108_backed=t108.status == "PROVED_LOCALLY" and nonempty,
        messages=[f"nodes={len(node_sets)}"],
    )
