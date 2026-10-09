"""Parameter-disconnected to nonsummable diffuse-end routes (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.cantor_parameter_support import audit_cantor_parameter_support
from squarepeg.global_geometry.cross_component_interactions import audit_cross_component_interactions
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits


@dataclass
class ParameterDiffuseRoute:
    limit_id: str
    routes_to_diffuse: bool
    destination: str


@dataclass
class ParameterToDiffuseEndRouteAudit:
    routes: list[ParameterDiffuseRoute]
    distinct_from_center: bool
    messages: list[str]


def audit_parameter_to_diffuse_end_routes(tree: CanonicalIntrusionTree) -> ParameterToDiffuseEndRouteAudit:
    limits = audit_parameter_disconnected_limits(tree)
    cantor = audit_cantor_parameter_support(tree)
    cross = audit_cross_component_interactions(tree)
    routes: list[ParameterDiffuseRoute] = []
    for r in limits.records:
        to_diffuse = False
        dest = "NONE"
        for cr in cantor.records:
            if cr.limit_id == r.limit_id and cr.route == "NONSUMMABLE_DIFFUSE_END":
                to_diffuse = True
                dest = "NONSUMMABLE_DIFFUSE_END_GEOMETRY"
        for cx in cross.records:
            if cx.interaction_id == r.limit_id and cx.interaction_class == "NONSUMMABLE_DIFFUSE":
                to_diffuse = True
                dest = "NONSUMMABLE_DIFFUSE_END_GEOMETRY"
        routes.append(ParameterDiffuseRoute(r.limit_id, to_diffuse, dest))
    return ParameterToDiffuseEndRouteAudit(routes, True, [f"n={len(routes)}"])
