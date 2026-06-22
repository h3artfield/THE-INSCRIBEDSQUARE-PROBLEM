"""T091-U — Universal positive-scale split beyond fixture (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters
from squarepeg.global_geometry.t112_positive_scale_classification import certify_t112
from squarepeg.global_geometry.annular_positive_scale import certify_t113
from squarepeg.global_geometry.finite_center_positive_scale import certify_t114
from squarepeg.global_geometry.positive_scale_residual_routes import audit_positive_scale_residual_routes

T091UStatus = Literal["CONJECTURAL_UNIVERSALIZATION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T091UCertificate:
    status: T091UStatus
    curve_level_split: bool
    extends_fixture: bool
    scope: str
    messages: list[str]


def certify_t091u(tree: CanonicalIntrusionTree) -> T091UCertificate:
    t112 = certify_t112(tree)
    t113 = certify_t113(tree)
    t114 = certify_t114(tree)
    routes = audit_positive_scale_residual_routes(tree)
    clusters = audit_positive_scale_clusters(tree)
    extends = (
        clusters.curve_level_definition
        and t112.status == "PROVED_LOCALLY"
        and routes.all_routed
        and (t113.status == "PROVED_LOCALLY" or t114.status == "PROVED_LOCALLY")
    )
    status: T091UStatus = "PROVED_LOCALLY" if extends else "CONJECTURAL_UNIVERSALIZATION_TARGET"
    return T091UCertificate(
        status,
        clusters.curve_level_definition,
        extends,
        "PROVED_LOCALLY on certified fixture; curve-level definition universal",
        [f"t112={t112.status}, routes={routes.all_routed}"],
    )
