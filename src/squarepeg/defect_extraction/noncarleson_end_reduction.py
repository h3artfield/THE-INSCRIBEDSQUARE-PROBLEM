"""T086R, T084C non-Carleson end reduction (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_end_surgery import certify_t087
from squarepeg.defect_extraction.finite_center_end_rigidity import certify_t089
from squarepeg.defect_extraction.frostman_end_criterion import certify_t090
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density
from squarepeg.defect_extraction.noncarleson_cantor_tangent import audit_noncarleson_cantor_tangent
from squarepeg.defect_extraction.t081i_proof import certify_t081i_v2
from squarepeg.defect_extraction.tangent_end_classifier import audit_tangent_end_classifier
from squarepeg.defect_extraction.tangent_tree_compactness import build_tangent_sequence

T086RStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T084CStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T086RRoute = Literal[
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_REDUCTION",
    "ATOMIC_RAY_TANGENT",
    "INFINITE_CENTER_TANGENT",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_END",
    "POSITIVE_SCALE_NONANNULAR",
    "NONCARLESON_CANTOR_END_TANGENT",
    "T087_CLOSED",
]

T084CRoute = Literal[
    "T080_T081I_T087_CLOSED",
    "T085_RAY",
    "T086R_TANGENT",
    "CANTOR_TANGENT",
    "GLOBAL_RESIDUAL",
]


@dataclass
class T086RCertificate:
    status: T086RStatus
    route: T086RRoute
    messages: list[str]


@dataclass
class T084CCertificate:
    status: T084CStatus
    route: T084CRoute
    messages: list[str]


def certify_t086r(tree: CanonicalIntrusionTree) -> T086RCertificate:
    """T086R — non-Carleson diffuse-end reduction via bad-cylinder tangents."""
    t087 = certify_t087(tree)
    nc = audit_noncarleson_end_density(tree)
    if t087.status == "PROVED_LOCALLY":
        return T086RCertificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="T087_CLOSED",
            messages=["Carleson satisfied"],
        )
    if not nc.intrinsically_non_carleson:
        return T086RCertificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="T087_CLOSED",
            messages=["not intrinsically non-Carleson"],
        )

    tangent = audit_tangent_end_classifier(tree, A=2.0)
    cantor = audit_noncarleson_cantor_tangent(tree)
    route: T086RRoute = "NONCARLESON_CANTOR_END_TANGENT"
    status: T086RStatus = "CONJECTURAL_STRUCTURAL_TARGET"

    if tangent.routes_t064:
        route = "CONCENTRATED_DESCENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif tangent.routes_t062:
        route = "FINITE_CENTER_REDUCTION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif tangent.routes_t085:
        route = "ATOMIC_RAY_TANGENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif tangent.primary == "INFINITE_CENTER":
        route = "INFINITE_CENTER_TANGENT"
    elif tangent.primary == "PARAMETER_DISCONNECTED":
        route = "PARAMETER_DISCONNECTED"
    elif tangent.primary == "NON_JORDAN":
        route = "NON_JORDAN_END"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif cantor.is_cantor_tangent:
        route = "NONCARLESON_CANTOR_END_TANGENT"

    return T086RCertificate(status=status, route=route, messages=[f"route={route}"])


def certify_t084c(tree: CanonicalIntrusionTree) -> T084CCertificate:
    """T084C — Cantor-end tree reduction."""
    t080 = certify_t080(tree)
    t081i = certify_t081i_v2(tree)
    t087 = certify_t087(tree)
    t086r = certify_t086r(tree)

    if t081i.status == "PROVED_LOCALLY" or t080.status == "PROVED_LOCALLY" or t087.status == "PROVED_LOCALLY":
        return T084CCertificate(
            status="PROVED_LOCALLY_PARTIAL",
            route="T080_T081I_T087_CLOSED",
            messages=["surgically closed"],
        )

    route: T084CRoute = "T086R_TANGENT"
    status: T084CStatus = "CONJECTURAL_TARGET"
    if t086r.route == "NONCARLESON_CANTOR_END_TANGENT":
        route = "CANTOR_TANGENT"
    elif t086r.status == "PROVED_LOCALLY_CLASSIFIER":
        route = "T086R_TANGENT"
        status = "PROVED_LOCALLY_PARTIAL"

    return T084CCertificate(status=status, route=route, messages=[f"route={route}"])
