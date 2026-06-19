"""T082F — Infinite-tree final reduction (Directive 043)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_tree_area_tightness import certify_t081_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.nonsummable_tree_classifier import certify_t084r
from squarepeg.defect_extraction.t081i_proof import certify_t081i_v2

T082FStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T082FRoute = Literal[
    "T080_SUMMABLE_RAY",
    "T081_LOCALLY_FINITE",
    "T081I_COUNTABLY_BRANCHING",
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_DECOMPOSITION",
    "NONSUMMABLE_RAY_T085",
    "DIFFUSE_END_T086",
    "INFINITE_CENTER_BRANCHING",
    "NON_JORDAN_HULL",
    "PARAMETER_DISCONNECTED",
    "POSITIVE_SCALE_NONANNULAR",
]


@dataclass
class T082FCertificate:
    status: T082FStatus
    route: T082FRoute
    t080: str
    t081: str
    t081i: str
    t084r: str
    surgically_closed: bool
    messages: list[str]


def certify_t082f(tree: CanonicalIntrusionTree) -> T082FCertificate:
    """Every infinite intrusion tree is surgically closed or in an exact residual class."""
    t080 = certify_t080(tree)
    t081 = certify_t081_v2(tree)
    t081i = certify_t081i_v2(tree)
    t084r = certify_t084r(tree)

    route: T082FRoute = "DIFFUSE_END_T086"
    status: T082FStatus = "CONJECTURAL_TARGET"
    closed = False

    if t081i.status == "PROVED_LOCALLY":
        route = "T081I_COUNTABLY_BRANCHING"
        status = "PROVED_LOCALLY_PARTIAL"
        closed = True
    elif t081.status == "PROVED_LOCALLY":
        route = "T081_LOCALLY_FINITE"
        status = "PROVED_LOCALLY_PARTIAL"
        closed = True
    elif t080.status == "PROVED_LOCALLY":
        route = "T080_SUMMABLE_RAY"
        status = "PROVED_LOCALLY_PARTIAL"
        closed = True
    elif t084r.route == "CONCENTRATED_DESCENT":
        route = "CONCENTRATED_DESCENT"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t084r.route == "FINITE_CENTER_DECOMPOSITION":
        route = "FINITE_CENTER_DECOMPOSITION"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t084r.route == "NONSUMMABLE_RAY_T085":
        route = "NONSUMMABLE_RAY_T085"
    elif t084r.route == "DIFFUSE_END_T086":
        route = "DIFFUSE_END_T086"
    elif t084r.route == "INFINITE_CENTER_BRANCHING":
        route = "INFINITE_CENTER_BRANCHING"
    elif t084r.route == "NON_JORDAN_HULL":
        route = "NON_JORDAN_HULL"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t084r.route == "PARAMETER_DISCONNECTED":
        route = "PARAMETER_DISCONNECTED"
    elif t084r.route == "POSITIVE_SCALE_NONANNULAR":
        route = "POSITIVE_SCALE_NONANNULAR"

    return T082FCertificate(
        status=status,
        route=route,
        t080=t080.status,
        t081=t081.status,
        t081i=t081i.status,
        t084r=t084r.route,
        surgically_closed=closed,
        messages=[f"route={route}, closed={closed}"],
    )
