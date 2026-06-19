"""T084, T082I infinite local branching reduction (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_tree_area_tightness import certify_t081_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_center_measure import audit_child_center_measures
from squarepeg.defect_extraction.child_l1_signature import audit_child_l1_signature_v2
from squarepeg.defect_extraction.diffuse_end_classifier import classify_diffuse_ends
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.nonsummable_child_node import audit_nonsummable_child_nodes
from squarepeg.defect_extraction.t081i_proof import certify_t081i_v2

T084Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T082IStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T084Route = Literal[
    "T081I_SUMMABLE",
    "CONCENTRATED_CHILD_DESCENT",
    "FINITE_CENTER_CHILD_DECOMPOSITION",
    "NONSUMMABLE_INTRUSION_RAY",
    "DIFFUSE_END_MEASURE",
    "INFINITE_CENTER_BRANCHING",
    "NON_JORDAN_HULL",
    "PARAMETER_DISCONNECTED",
    "POSITIVE_SCALE_NONANNULAR",
]


@dataclass
class T084Certificate:
    status: T084Status
    route: T084Route
    messages: list[str]


@dataclass
class T082ICertificate:
    status: T082IStatus
    route: str
    t080: str
    t081: str
    t081i: str
    messages: list[str]


def certify_t084(tree: CanonicalIntrusionTree) -> T084Certificate:
    t081i = certify_t081i_v2(tree)
    l1 = audit_child_l1_signature_v2(tree)
    centers = audit_child_center_measures(tree)
    ns = audit_nonsummable_child_nodes(tree)
    ends = classify_diffuse_ends(tree)
    route: T084Route = "DIFFUSE_END_MEASURE"
    status: T084Status = "CONJECTURAL_STRUCTURAL_TARGET"
    if t081i.status == "PROVED_LOCALLY":
        route = "T081I_SUMMABLE"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.routes_t064:
        route = "CONCENTRATED_CHILD_DESCENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.routes_t062:
        route = "FINITE_CENTER_CHILD_DECOMPOSITION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif ns.any_nonsummable:
        route = "NONSUMMABLE_INTRUSION_RAY"
    elif ends.diffuse_end_tree:
        route = "DIFFUSE_END_MEASURE"
    elif centers.diffuse_child:
        route = "INFINITE_CENTER_BRANCHING"
    return T084Certificate(status=status, route=route, messages=[f"route={route}"])


def certify_t082i(tree: CanonicalIntrusionTree) -> T082ICertificate:
    t080 = certify_t080(tree)
    t081 = certify_t081_v2(tree)
    t081i = certify_t081i_v2(tree)
    t084 = certify_t084(tree)
    route = t084.route
    status: T082IStatus = "CONJECTURAL_TARGET"
    if t081i.status == "PROVED_LOCALLY":
        route = "T081I_COUNTABLY_BRANCHING"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t081.status == "PROVED_LOCALLY":
        route = "T081_LOCALLY_FINITE"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t080.status == "PROVED_LOCALLY":
        route = "T080_SUMMABLE_RAY"
        status = "PROVED_LOCALLY_PARTIAL"
    return T082ICertificate(
        status=status,
        route=str(route),
        t080=t080.status,
        t081=t081.status,
        t081i=t081i.status,
        messages=[f"route={route}"],
    )
