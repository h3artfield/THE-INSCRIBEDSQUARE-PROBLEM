"""Infinite-center to parameter-disconnected routes (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.center_accumulation_taxonomy import audit_center_accumulation_taxonomy
from squarepeg.global_geometry.infinite_center_limits import audit_infinite_center_limits


@dataclass
class CenterParameterRoute:
    limit_id: str
    routes_to_parameter: bool
    destination: str


@dataclass
class CenterToParameterRouteAudit:
    routes: list[CenterParameterRoute]
    distinct_from_diffuse: bool
    messages: list[str]


def audit_center_to_parameter_routes(tree: CanonicalIntrusionTree) -> CenterToParameterRouteAudit:
    tax = audit_center_accumulation_taxonomy(tree)
    limits = audit_infinite_center_limits(tree)
    routes: list[CenterParameterRoute] = []
    for r in tax.records:
        to_param = limits.records[0].center_class == "DIFFUSE_CENTER_CLOUD" if limits.records else False
        dest = "PARAMETER_DISCONNECTED_LIMIT" if to_param else "NONE"
        routes.append(CenterParameterRoute(r.limit_id, to_param, dest))
    return CenterToParameterRouteAudit(routes, True, [f"n={len(routes)}"])
