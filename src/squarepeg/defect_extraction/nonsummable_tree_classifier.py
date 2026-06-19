"""T084R — Nonsummable child and end reduction (Directive 043)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_signature_concentration import audit_child_signature_concentration
from squarepeg.defect_extraction.diffuse_end_geometry import certify_t086
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.intrinsic_tree_nonsummability import audit_intrinsic_tree_nonsummability
from squarepeg.defect_extraction.nonsummable_ray_reduction import certify_t085
from squarepeg.defect_extraction.t081i_proof import certify_t081i_v2

T084RStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]

T084RRoute = Literal[
    "T081I_SUMMABLE",
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_DECOMPOSITION",
    "NONSUMMABLE_RAY_T085",
    "DIFFUSE_END_T086",
    "INFINITE_CENTER_BRANCHING",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_HULL",
    "POSITIVE_SCALE_NONANNULAR",
]


@dataclass
class T084RCertificate:
    status: T084RStatus
    route: T084RRoute
    nonsummable: bool
    messages: list[str]


def certify_t084r(tree: CanonicalIntrusionTree) -> T084RCertificate:
    """Every tree failing T080/T081/T081I admits a classified subtree route."""
    t081i = certify_t081i_v2(tree)
    t080 = certify_t080(tree)
    intrinsic = audit_intrinsic_tree_nonsummability(tree)
    centers = audit_child_signature_concentration(tree)
    t085 = certify_t085(tree)
    t086 = certify_t086(tree)

    if t081i.status == "PROVED_LOCALLY":
        return T084RCertificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="T081I_SUMMABLE",
            nonsummable=False,
            messages=["surgically closed via T081I"],
        )
    if t080.status == "PROVED_LOCALLY":
        return T084RCertificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="T081I_SUMMABLE",
            nonsummable=False,
            messages=["surgically closed via T080"],
        )

    nonsummable = intrinsic.summability != "SUMMABLE"
    route: T084RRoute = "DIFFUSE_END_T086"
    status: T084RStatus = "CONJECTURAL_STRUCTURAL_TARGET"

    if centers.routes_t064:
        route = "CONCENTRATED_DESCENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.routes_t062:
        route = "FINITE_CENTER_DECOMPOSITION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.hull_degenerate:
        route = "NON_JORDAN_HULL"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif t085.nonsummable:
        route = "NONSUMMABLE_RAY_T085"
        if t085.status == "PROVED_LOCALLY_CLASSIFIER":
            status = "PROVED_LOCALLY_CLASSIFIER"
    elif intrinsic.failure_class == "RAY_SIGNATURE_NONSUMMABILITY":
        route = "NONSUMMABLE_RAY_T085"
    elif t086.route in ("CANTOR_END_RESIDUAL", "INFINITE_CENTER_PROLIFERATION"):
        route = "DIFFUSE_END_T086" if t086.route == "CANTOR_END_RESIDUAL" else "INFINITE_CENTER_BRANCHING"
    elif t086.route == "SPATIAL_CONCENTRATION":
        route = "CONCENTRATED_DESCENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.diffuse_child_center:
        route = "INFINITE_CENTER_BRANCHING"

    return T084RCertificate(
        status=status,
        route=route,
        nonsummable=nonsummable,
        messages=[f"route={route}, nonsummable={nonsummable}"],
    )
