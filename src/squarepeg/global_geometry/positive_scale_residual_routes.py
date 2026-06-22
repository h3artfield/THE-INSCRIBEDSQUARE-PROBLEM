"""Positive-scale residual routes (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.annular_positive_scale import audit_annular_positive_scale
from squarepeg.global_geometry.finite_center_positive_scale import audit_finite_center_positive_scale
from squarepeg.global_geometry.nonannular_cluster_classifier import audit_nonannular_cluster_classifier
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters

RouteKind = Literal["SOLVED", "GLOBAL_RESIDUAL", "UNROUTED"]


@dataclass
class PositiveScaleRoute:
    cluster_id: str
    route: str
    kind: RouteKind
    destination: str


@dataclass
class PositiveScaleRouteAudit:
    routes: list[PositiveScaleRoute]
    all_routed: bool
    no_new_residual: bool
    messages: list[str]


def audit_positive_scale_residual_routes(tree: CanonicalIntrusionTree) -> PositiveScaleRouteAudit:
    clusters = audit_positive_scale_clusters(tree)
    ann = audit_annular_positive_scale(tree)
    fin = audit_finite_center_positive_scale(tree)
    non = audit_nonannular_cluster_classifier(tree)
    routes: list[PositiveScaleRoute] = []
    for c in clusters.clusters:
        if c.split == "ANNULAR" and ann.hypotheses_satisfied:
            routes.append(PositiveScaleRoute(c.cluster_id, "annular", "SOLVED", ann.destination))
        elif fin.finite_center:
            routes.append(PositiveScaleRoute(c.cluster_id, "finite_center", "SOLVED", fin.destination))
        else:
            nc = next((x for x in non.classifications if x.cluster_id == c.cluster_id), None)
            if nc and nc.reduces_to_global:
                routes.append(PositiveScaleRoute(c.cluster_id, "nonannular", "GLOBAL_RESIDUAL", nc.reduces_to_global))
            elif nc and nc.failure_class == "NOT_NONANNULAR":
                routes.append(PositiveScaleRoute(c.cluster_id, "annular_or_solved", "SOLVED", "T091"))
            else:
                routes.append(PositiveScaleRoute(c.cluster_id, "persistent", "GLOBAL_RESIDUAL", "POSITIVE_SCALE_NONANNULAR_CLUSTER"))
    all_r = all(r.kind != "UNROUTED" for r in routes) and bool(routes or not clusters.positive_mass)
    new_residual = any(r.destination not in (
        "T062", "T091", "PROTECTED_SQUARE", "T036-N3-ANN", "T042",
        "NON_JORDAN_SATURATION_HULL", "PARAMETER_DISCONNECTED_LIMIT",
        "INFINITE_CENTER_GEOMETRY", "POSITIVE_SCALE_NONANNULAR_CLUSTER",
    ) for r in routes)
    return PositiveScaleRouteAudit(routes, all_r, not new_residual, [f"n={len(routes)}"])
