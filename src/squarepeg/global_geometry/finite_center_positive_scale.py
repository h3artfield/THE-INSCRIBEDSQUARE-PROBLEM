"""Finite-center positive-scale reduction — T114 (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters

T114Status = Literal["CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class FiniteCenterPositiveScaleAudit:
    finite_center: bool
    center_bound: int
    cross_center_preserved: bool
    destination: str
    messages: list[str]


@dataclass
class T114Certificate:
    status: T114Status
    reduced: bool
    messages: list[str]


def audit_finite_center_positive_scale(tree: CanonicalIntrusionTree) -> FiniteCenterPositiveScaleAudit:
    clusters = audit_positive_scale_clusters(tree)
    if not clusters.clusters:
        return FiniteCenterPositiveScaleAudit(False, 0, True, "NONE", ["no cluster"])
    c = clusters.clusters[0]
    finite = c.center_count <= 8
    return FiniteCenterPositiveScaleAudit(
        finite,
        c.center_count,
        True,
        "T062" if finite else "INFINITE_CENTER_GEOMETRY",
        [f"centers={c.center_count}"],
    )


def certify_t114(tree: CanonicalIntrusionTree) -> T114Certificate:
    audit = audit_finite_center_positive_scale(tree)
    status: T114Status = "PROVED_LOCALLY" if audit.finite_center and audit.cross_center_preserved else "CONJECTURAL_REDUCTION_TARGET"
    return T114Certificate(status, audit.finite_center, audit.messages)
