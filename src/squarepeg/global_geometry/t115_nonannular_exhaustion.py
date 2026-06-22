"""T115 — Nonannular positive-scale residual exhaustion (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.nonannular_cluster_classifier import audit_nonannular_cluster_classifier
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters
from squarepeg.global_geometry.positive_scale_residual_routes import audit_positive_scale_residual_routes

T115Status = Literal["CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS"]


@dataclass
class T115Certificate:
    status: T115Status
    exhausted: bool
    narrow_residual: bool
    messages: list[str]


def certify_t115(tree: CanonicalIntrusionTree) -> T115Certificate:
    clusters = audit_positive_scale_clusters(tree)
    routes = audit_positive_scale_residual_routes(tree)
    non = audit_nonannular_cluster_classifier(tree)
    has_nonannular = any(c.split == "NONANNULAR" for c in clusters.clusters)
    persistent = any(r.destination == "POSITIVE_SCALE_NONANNULAR_CLUSTER" for r in routes.routes)
    if not has_nonannular:
        status: T115Status = "PROVED_LOCALLY"
        exhausted = True
        narrow = False
    elif persistent and routes.all_routed:
        status = "NARROW_RESIDUAL_REMAINS"
        exhausted = False
        narrow = True
    elif routes.all_routed:
        status = "PROVED_LOCALLY"
        exhausted = True
        narrow = False
    else:
        status = "CONJECTURAL_EXHAUSTION_TARGET"
        exhausted = False
        narrow = False
    return T115Certificate(status, exhausted, narrow, [f"has_nonannular={has_nonannular}, persistent={persistent}"])
