"""T086, T084E, T088 diffuse end reduction (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_end_surgery import certify_t087
from squarepeg.defect_extraction.end_concentration import audit_end_concentration
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2
from squarepeg.defect_extraction.end_spatial_map import audit_end_parameter_map, audit_end_spatial_map
from squarepeg.defect_extraction.infinite_center_end_geometry import audit_infinite_center_end_geometry
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.nonsummable_ray_reduction import certify_t085
from squarepeg.defect_extraction.t081i_proof import certify_t081i_v2

T086Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T084EStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T088Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]

T086Route = Literal[
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_DECOMPOSITION",
    "T087_DIFFUSE_SURGERY",
    "INFINITE_CENTER_BRANCHING",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_END",
    "CANTOR_END_RESIDUAL",
    "SUMMABLE_CLOSED",
]

T084ERoute = Literal[
    "T080_T081I_CLOSED",
    "T085_RAY",
    "T087_END",
    "CONCENTRATED",
    "FINITE_CENTER",
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "CANTOR_RESIDUAL",
]

T088Route = Literal[
    "T087_PROMOTED",
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_SUBSEQUENCE",
    "INFINITE_CENTER",
    "NON_JORDAN",
]


@dataclass
class T086Certificate:
    status: T086Status
    route: T086Route
    messages: list[str]


@dataclass
class T084ECertificate:
    status: T084EStatus
    route: T084ERoute
    messages: list[str]


@dataclass
class T088Certificate:
    status: T088Status
    route: T088Route
    messages: list[str]


def certify_t086_v2(tree: CanonicalIntrusionTree) -> T086Certificate:
    """T086 — diffuse end structural theorem."""
    t080 = certify_t080(tree)
    t081i = certify_t081i_v2(tree)
    t087 = certify_t087(tree)
    conc = audit_end_concentration(tree)
    spatial = audit_end_spatial_map(tree)
    param = audit_end_parameter_map(tree)
    em = build_end_signature_measure_v2(tree)
    carl = audit_end_signature_carleson(tree)
    ic = audit_infinite_center_end_geometry(tree)

    if t081i.status == "PROVED_LOCALLY" or t080.status == "PROVED_LOCALLY":
        return T086Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="SUMMABLE_CLOSED",
            messages=["T080/T081I closed"],
        )

    route: T086Route = "CANTOR_END_RESIDUAL"
    status: T086Status = "CONJECTURAL_STRUCTURAL_TARGET"

    if t087.status == "PROVED_LOCALLY":
        route = "T087_DIFFUSE_SURGERY"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif conc.routes_t064:
        route = "CONCENTRATED_DESCENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif conc.routes_t062:
        route = "FINITE_CENTER_DECOMPOSITION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif param.disconnected:
        route = "PARAMETER_DISCONNECTED"
    elif spatial.records and any(r.spatial_class == "NON_JORDAN_END_DEGENERATION" for r in spatial.records):
        route = "NON_JORDAN_END"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif ic.infinite_center:
        route = "INFINITE_CENTER_BRANCHING"
    elif em.continuous_mass > 0 and not carl.satisfies_carleson:
        route = "CANTOR_END_RESIDUAL"

    return T086Certificate(status=status, route=route, messages=[f"route={route}"])


def certify_t084e(tree: CanonicalIntrusionTree) -> T084ECertificate:
    """T084E — end-measure nonsummable tree reduction."""
    t086 = certify_t086_v2(tree)
    t085 = certify_t085(tree)
    t087 = certify_t087(tree)
    t081i = certify_t081i_v2(tree)

    if t081i.status == "PROVED_LOCALLY":
        return T084ECertificate(
            status="PROVED_LOCALLY_PARTIAL",
            route="T080_T081I_CLOSED",
            messages=["surgically closed"],
        )

    route: T084ERoute = "CANTOR_RESIDUAL"
    status: T084EStatus = "CONJECTURAL_TARGET"

    if t087.status == "PROVED_LOCALLY":
        route = "T087_END"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t085.nonsummable and t085.status == "PROVED_LOCALLY_CLASSIFIER":
        route = "T085_RAY"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t086.route == "CONCENTRATED_DESCENT":
        route = "CONCENTRATED"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t086.route == "FINITE_CENTER_DECOMPOSITION":
        route = "FINITE_CENTER"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t086.route == "INFINITE_CENTER_BRANCHING":
        route = "INFINITE_CENTER"
    elif t086.route == "CANTOR_END_RESIDUAL":
        route = "CANTOR_RESIDUAL"

    return T084ECertificate(status=status, route=route, messages=[f"route={route}"])


def certify_t088(tree: CanonicalIntrusionTree) -> T088Certificate:
    """T088 — diffuse child-to-end promotion."""
    from squarepeg.defect_extraction.child_signature_concentration import audit_child_signature_concentration

    child = audit_child_signature_concentration(tree)
    t087 = certify_t087(tree)
    ic = audit_infinite_center_end_geometry(tree)

    route: T088Route = "INFINITE_CENTER"
    status: T088Status = "CONJECTURAL_STRUCTURAL_TARGET"

    if t087.status == "PROVED_LOCALLY":
        route = "T087_PROMOTED"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif child.routes_t064:
        route = "CONCENTRATED_DESCENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif child.routes_t062:
        route = "FINITE_CENTER_SUBSEQUENCE"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif ic.infinite_center:
        route = "INFINITE_CENTER"
    elif child.hull_degenerate:
        route = "NON_JORDAN"
        status = "PROVED_LOCALLY_CLASSIFIER"

    return T088Certificate(status=status, route=route, messages=[f"route={route}"])
