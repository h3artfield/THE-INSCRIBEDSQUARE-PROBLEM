"""Route-set topology and closure (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_transition_routes import (
    AugmentedRoute,
    audit_augmented_transition_routes,
)
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

RouteTopology = Literal["CLOSED", "OPEN_WITH_MARGIN", "COUNTABLE_UNION_OF_CLOSED", "NOT_CLOSED"]


@dataclass
class RouteSetRecord:
    route: AugmentedRoute
    topology: RouteTopology
    measurable: bool


@dataclass
class RouteSetTopologyAudit:
    records: list[RouteSetRecord]
    all_measurable: bool
    all_closed_or_margined: bool
    messages: list[str]


_ROUTE_TOPOLOGY: dict[AugmentedRoute, RouteTopology] = {
    "R_SUMMABLE_CHILD": "CLOSED",
    "R_ORDERED_GATE": "CLOSED",
    "R_FINITE_WIDTH_ORDER": "CLOSED",
    "R_COUNTABLE_ORDER": "COUNTABLE_UNION_OF_CLOSED",
    "R_CONCENTRATION": "CLOSED",
    "R_FINITE_CENTER": "CLOSED",
    "R_INFINITE_CENTER": "OPEN_WITH_MARGIN",
    "R_INFINITE_TREE": "CLOSED",
    "R_PARAMETER_DISCONNECTED": "CLOSED",
    "R_COLLISION_DEGENERATION": "CLOSED",
    "R_POSITIVE_SCALE": "CLOSED",
    "UNROUTED": "NOT_CLOSED",
}


def audit_route_set_topology(tree: CanonicalIntrusionTree) -> RouteSetTopologyAudit:
    routes = audit_augmented_transition_routes(tree)
    seen: set[AugmentedRoute] = set()
    records: list[RouteSetRecord] = []
    for r in routes.records:
        if r.route in seen:
            continue
        seen.add(r.route)
        topo = _ROUTE_TOPOLOGY.get(r.route, "NOT_CLOSED")
        records.append(RouteSetRecord(r.route, topo, topo != "NOT_CLOSED"))
    all_m = all(r.measurable for r in records)
    all_c = all(r.topology != "NOT_CLOSED" for r in records)
    return RouteSetTopologyAudit(
        records=records,
        all_measurable=all_m,
        all_closed_or_margined=all_c and routes.all_routed,
        messages=[f"routes={len(records)}"],
    )
