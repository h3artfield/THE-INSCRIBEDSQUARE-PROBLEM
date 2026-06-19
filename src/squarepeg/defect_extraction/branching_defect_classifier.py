"""Branching defect allocation classifier (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.intrusion_ray_geometry import extract_ray
from squarepeg.defect_extraction.tree_attachment_identity import child_join_term

BranchingRoute = Literal[
    "DOMINANT_CHILD",
    "FINITE_CENTER_CHILD_FAMILY",
    "DIFFUSE_BRANCHING",
    "JOIN_DOMINATED",
    "CANCELLATION_DOMINATED",
]


@dataclass
class NodeBranchingClass:
    node_id: str
    route: BranchingRoute
    dominant_fraction: float
    center_count: int
    join_fraction: float


@dataclass
class BranchingDefectAudit:
    node_classes: list[NodeBranchingClass]
    primary_route: BranchingRoute
    routes_to_t080: bool
    routes_to_t062: bool
    messages: list[str]


def classify_node_branching(
    tree: CanonicalIntrusionTree,
    nid: str,
) -> NodeBranchingClass:
    node = tree.nodes[nid]
    children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
    if not children:
        return NodeBranchingClass(nid, "DOMINANT_CHILD", 1.0, 1, 0.0)
    defects = [c.defect for c in children]
    total = sum(defects) or 1.0
    max_frac = max(defects) / total
    join = child_join_term(node, children)
    join_frac = join.join_area / max(total, 1e-9)
    centers = len({(round(c.center[0], 1), round(c.center[1], 1)) for c in children})
    pos = sum(d for d in defects if d > 0)
    neg = sum(-d for d in defects if d < 0)
    route: BranchingRoute = "DIFFUSE_BRANCHING"
    if max_frac >= 0.5:
        route = "DOMINANT_CHILD"
    elif centers <= 3:
        route = "FINITE_CENTER_CHILD_FAMILY"
    elif join_frac >= 0.35:
        route = "JOIN_DOMINATED"
    elif pos > 0.1 and neg > 0.1:
        route = "CANCELLATION_DOMINATED"
    return NodeBranchingClass(nid, route, max_frac, centers, join_frac)


def audit_branching_defects(tree: CanonicalIntrusionTree) -> BranchingDefectAudit:
    classes = [
        classify_node_branching(tree, nid)
        for nid, node in tree.nodes.items()
        if node.child_ids
    ]
    primary: BranchingRoute = "DIFFUSE_BRANCHING"
    if classes:
        primary = max(classes, key=lambda c: c.dominant_fraction).route
    t080 = certify_t080(tree)
    ray = extract_ray(tree)
    routes_t080 = primary == "DOMINANT_CHILD" and t080.status == "PROVED_LOCALLY"
    routes_t062 = primary == "FINITE_CENTER_CHILD_FAMILY"
    return BranchingDefectAudit(
        node_classes=classes,
        primary_route=primary,
        routes_to_t080=routes_t080,
        routes_to_t062=routes_t062,
        messages=[f"primary={primary}, t080={routes_t080}"],
    )
