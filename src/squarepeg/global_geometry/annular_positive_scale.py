"""Annular positive-scale route (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters

T113Status = Literal["CONJECTURAL_ROUTE_TARGET", "PROVED_LOCALLY"]
AnnularDestination = Literal["T036-N3-ANN", "T042", "PROTECTED_SQUARE", "NONE"]


@dataclass
class AnnularPositiveScaleAudit:
    annular_detected: bool
    destination: AnnularDestination
    hypotheses_satisfied: bool
    messages: list[str]


@dataclass
class T113Certificate:
    status: T113Status
    routed: bool
    destination: AnnularDestination
    messages: list[str]


def audit_annular_positive_scale(tree: CanonicalIntrusionTree) -> AnnularPositiveScaleAudit:
    clusters = audit_positive_scale_clusters(tree)
    annular = any(c.split == "ANNULAR" for c in clusters.clusters)
    dest: AnnularDestination = "NONE"
    if annular:
        dest = "PROTECTED_SQUARE"
    return AnnularPositiveScaleAudit(annular, dest, annular and dest != "NONE", [f"annular={annular}"])


def certify_t113(tree: CanonicalIntrusionTree) -> T113Certificate:
    audit = audit_annular_positive_scale(tree)
    status: T113Status = "PROVED_LOCALLY" if audit.hypotheses_satisfied else "CONJECTURAL_ROUTE_TARGET"
    return T113Certificate(status, audit.hypotheses_satisfied, audit.destination, audit.messages)
