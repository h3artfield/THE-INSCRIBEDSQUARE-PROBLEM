"""Nonannular positive-scale cluster classifier (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters

NonannularClass = Literal[
    "HULL_PINCHING",
    "PARAMETER_DISCONNECTED",
    "CENTER_PROLIFERATION",
    "NON_JORDAN_SATURATION",
    "PERSISTENT_NONANNULAR",
    "NOT_NONANNULAR",
]


@dataclass
class NonannularClassification:
    cluster_id: str
    failure_class: NonannularClass
    reduces_to_global: str | None


@dataclass
class NonannularClusterClassifierAudit:
    classifications: list[NonannularClassification]
    exhaustive: bool
    messages: list[str]


def audit_nonannular_cluster_classifier(tree: CanonicalIntrusionTree) -> NonannularClusterClassifierAudit:
    clusters = audit_positive_scale_clusters(tree)
    t091 = certify_t091(tree)
    out: list[NonannularClassification] = []
    for c in clusters.clusters:
        if c.split != "NONANNULAR":
            out.append(NonannularClassification(c.cluster_id, "NOT_NONANNULAR", None))
            continue
        fc: NonannularClass = "PERSISTENT_NONANNULAR"
        global_name = "POSITIVE_SCALE_NONANNULAR_CLUSTER"
        if not c.parameter_connected:
            fc = "PARAMETER_DISCONNECTED"
            global_name = "PARAMETER_DISCONNECTED_LIMIT"
        elif not c.jordan:
            fc = "NON_JORDAN_SATURATION"
            global_name = "NON_JORDAN_SATURATION_HULL"
        elif c.center_count > 8:
            fc = "CENTER_PROLIFERATION"
            global_name = "INFINITE_CENTER_GEOMETRY"
        elif t091.route == "INCOMPATIBLE_NESTED_HULLS":
            fc = "HULL_PINCHING"
            global_name = "NON_JORDAN_SATURATION_HULL"
        out.append(NonannularClassification(c.cluster_id, fc, global_name))
    exhaustive = all(x.failure_class != "NOT_NONANNULAR" or clusters.clusters for x in out) or not clusters.clusters
    return NonannularClusterClassifierAudit(out, exhaustive, [f"n={len(out)}"])
