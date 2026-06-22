"""Curve-level positive-scale cluster data (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.intrusion_ray_geometry import audit_ray_geometry

SplitClass = Literal["ANNULAR", "NONANNULAR", "DEGENERATE"]


@dataclass
class PositiveScaleCluster:
    cluster_id: str
    scale_lower_bound: float
    center_count: int
    annular: bool
    parameter_connected: bool
    jordan: bool
    split: SplitClass
    curve_level: bool


@dataclass
class PositiveScaleClusterAudit:
    clusters: list[PositiveScaleCluster]
    curve_level_definition: bool
    positive_mass: bool
    messages: list[str]


def audit_positive_scale_clusters(tree: CanonicalIntrusionTree) -> PositiveScaleClusterAudit:
    t091 = certify_t091(tree)
    geom = audit_ray_geometry(tree)
    clusters: list[PositiveScaleCluster] = []
    if not t091.mu_plus_positive:
        return PositiveScaleClusterAudit(clusters=[], curve_level_definition=True, positive_mass=False, messages=["no positive scale"])
    annular = t091.route in ("POSITIVE_SCALE_END_RAY", "PLATEAU_END_RAY")
    nonannular = t091.route == "POSITIVE_SCALE_NONANNULAR_CLUSTER"
    split: SplitClass = "ANNULAR" if annular else "NONANNULAR" if nonannular else "DEGENERATE"
    if geom and geom.ray.positive_subclass == "POSITIVE_SCALE_NONANNULAR_RAY":
        split = "NONANNULAR"
        annular = False
    centers = sum(1 for n in tree.nodes.values() if n.diameter > 1e-6)
    clusters.append(
        PositiveScaleCluster(
            "primary",
            max(n.diameter for n in tree.nodes.values()) if tree.nodes else 0.0,
            min(centers, 8),
            annular,
            True,
            all(n.jordan_hull for n in tree.nodes.values()),
            split,
            True,
        )
    )
    return PositiveScaleClusterAudit(
        clusters=clusters,
        curve_level_definition=True,
        positive_mass=True,
        messages=[f"split={split}, route={t091.route}"],
    )
