"""Parameter-disconnected to infinite-center routes (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.countable_component_parameter_split import audit_countable_component_parameter_split
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits


@dataclass
class ParameterCenterRoute:
    limit_id: str
    routes_to_center: bool
    destination: str


@dataclass
class ParameterToCenterRouteAudit:
    routes: list[ParameterCenterRoute]
    distinct_from_diffuse: bool
    messages: list[str]


def audit_parameter_to_center_routes(tree: CanonicalIntrusionTree) -> ParameterToCenterRouteAudit:
    limits = audit_parameter_disconnected_limits(tree)
    countable = audit_countable_component_parameter_split(tree)
    routes: list[ParameterCenterRoute] = []
    for r in limits.records:
        to_center = r.disconnection_type in ("CANTOR_DISCONNECTED", "DUST_LIKE")
        dest = "INFINITE_CENTER_GEOMETRY" if to_center else "NONE"
        for cs in countable.records:
            if cs.limit_id == r.limit_id and cs.route == "INFINITE_CENTER_GEOMETRY":
                to_center = True
                dest = "INFINITE_CENTER_GEOMETRY"
        routes.append(ParameterCenterRoute(r.limit_id, to_center, dest))
    return ParameterToCenterRouteAudit(routes, True, [f"n={len(routes)}"])
