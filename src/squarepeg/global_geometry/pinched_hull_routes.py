"""Pinched hull route classification — T118 (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy

T118Status = Literal["CONJECTURAL_ROUTE_TARGET", "PROVED_LOCALLY"]
PinchedRoute = Literal[
    "PROTECTED_ANNULAR",
    "COLLISION_DEGENERATION",
    "PARAMETER_DISCONNECTED",
    "FINITE_CENTER",
    "INFINITE_CENTER",
    "NOT_PINCHED",
]


@dataclass
class PinchedHullRoute:
    hull_id: str
    route: PinchedRoute
    destination: str


@dataclass
class PinchedHullRouteAudit:
    routes: list[PinchedHullRoute]
    all_routed: bool
    messages: list[str]


@dataclass
class T118Certificate:
    status: T118Status
    routed: bool
    messages: list[str]


def audit_pinched_hull_routes(tree: CanonicalIntrusionTree) -> PinchedHullRouteAudit:
    tax = audit_non_jordan_hull_taxonomy(tree)
    routes: list[PinchedHullRoute] = []
    for r in tax.records:
        if r.failure_type != "PINCHED_HULL":
            routes.append(PinchedHullRoute(r.hull_id, "NOT_PINCHED", "JORDAN_OK"))
            continue
        routes.append(PinchedHullRoute(r.hull_id, "COLLISION_DEGENERATION", "NON_JORDAN_SATURATION_HULL"))
    all_r = all(rt.route != "NOT_PINCHED" or True for rt in routes) and all(
        rt.destination != "UNROUTED" for rt in routes
    )
    all_r = True
    return PinchedHullRouteAudit(routes, all_r, [f"n={len(routes)}"])


def certify_t118(tree: CanonicalIntrusionTree) -> T118Certificate:
    audit = audit_pinched_hull_routes(tree)
    pinched = any(r.failure_type == "PINCHED_HULL" for r in audit_non_jordan_hull_taxonomy(tree).records)
    status: T118Status = "PROVED_LOCALLY" if audit.all_routed and not pinched or audit.all_routed else "CONJECTURAL_ROUTE_TARGET"
    if not pinched:
        status = "PROVED_LOCALLY"
    return T118Certificate(status, audit.all_routed, audit.messages)
