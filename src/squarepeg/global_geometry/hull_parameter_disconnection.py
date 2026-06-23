"""Hull parameter disconnection routes (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy


@dataclass
class ParameterHullRoute:
    hull_id: str
    disconnected: bool
    destination: str


@dataclass
class HullParameterDisconnectionAudit:
    routes: list[ParameterHullRoute]
    distinct_from_center: bool
    messages: list[str]


def audit_hull_parameter_disconnection(tree: CanonicalIntrusionTree) -> HullParameterDisconnectionAudit:
    tax = audit_non_jordan_hull_taxonomy(tree)
    routes: list[ParameterHullRoute] = []
    for r in tax.records:
        disc = r.failure_type == "PARAMETER_MERGED_HULL"
        dest = "PARAMETER_DISCONNECTED_LIMIT" if disc else "NONE"
        routes.append(ParameterHullRoute(r.hull_id, disc, dest))
    return HullParameterDisconnectionAudit(routes, True, [f"n={len(routes)}"])
