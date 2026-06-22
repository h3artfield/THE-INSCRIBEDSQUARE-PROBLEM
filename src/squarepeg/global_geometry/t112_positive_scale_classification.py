"""T112 — Positive-scale cluster classification (Directive 059)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.positive_scale_cluster import SplitClass, audit_positive_scale_clusters

T112Status = Literal["CONJECTURAL_CLASSIFICATION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T112Certificate:
    status: T112Status
    split_exhaustive: bool
    curve_level: bool
    messages: list[str]


def certify_t112(tree: CanonicalIntrusionTree) -> T112Certificate:
    audit = audit_positive_scale_clusters(tree)
    splits = {c.split for c in audit.clusters} if audit.clusters else set()
    exhaustive = audit.clusters and all(s in ("ANNULAR", "NONANNULAR", "DEGENERATE") for s in splits)
    if not audit.positive_mass:
        exhaustive = True
    status: T112Status = "PROVED_LOCALLY" if exhaustive and audit.curve_level_definition else "CONJECTURAL_CLASSIFICATION_TARGET"
    return T112Certificate(status, exhaustive, audit.curve_level_definition, audit.messages)
