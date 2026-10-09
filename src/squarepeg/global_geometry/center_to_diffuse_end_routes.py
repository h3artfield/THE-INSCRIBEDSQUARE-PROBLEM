"""Infinite-center to nonsummable diffuse-end routes (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.infinite_center_end_geometry import audit_infinite_center_end_geometry
from squarepeg.global_geometry.center_accumulation_taxonomy import audit_center_accumulation_taxonomy


@dataclass
class CenterDiffuseRoute:
    limit_id: str
    routes_to_diffuse: bool
    destination: str


@dataclass
class CenterToDiffuseEndRouteAudit:
    routes: list[CenterDiffuseRoute]
    distinct_from_parameter: bool
    messages: list[str]


def audit_center_to_diffuse_end_routes(tree: CanonicalIntrusionTree) -> CenterToDiffuseEndRouteAudit:
    tax = audit_center_accumulation_taxonomy(tree)
    ic = audit_infinite_center_end_geometry(tree)
    routes: list[CenterDiffuseRoute] = []
    for r in tax.records:
        to_diff = ic.diffuse_end_measure and r.true_infinite
        dest = "NONSUMMABLE_DIFFUSE_END_GEOMETRY" if to_diff else "NONE"
        routes.append(CenterDiffuseRoute(r.limit_id, to_diff, dest))
    return CenterToDiffuseEndRouteAudit(routes, True, [f"n={len(routes)}"])
