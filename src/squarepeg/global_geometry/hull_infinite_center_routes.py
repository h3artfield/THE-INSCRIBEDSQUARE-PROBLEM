"""Hull infinite-center routes (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy


@dataclass
class InfiniteCenterHullRoute:
    hull_id: str
    infinite_center: bool
    destination: str


@dataclass
class HullInfiniteCenterRouteAudit:
    routes: list[InfiniteCenterHullRoute]
    distinct_from_parameter: bool
    messages: list[str]


def audit_hull_infinite_center_routes(tree: CanonicalIntrusionTree) -> HullInfiniteCenterRouteAudit:
    tax = audit_non_jordan_hull_taxonomy(tree)
    routes: list[InfiniteCenterHullRoute] = []
    for r in tax.records:
        ic = r.failure_type == "INFINITE_CENTER_ACCUMULATION"
        dest = "INFINITE_CENTER_GEOMETRY" if ic else "NONE"
        routes.append(InfiniteCenterHullRoute(r.hull_id, ic, dest))
    return HullInfiniteCenterRouteAudit(routes, True, [f"n={len(routes)}"])
