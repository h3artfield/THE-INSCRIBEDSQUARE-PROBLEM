"""T116 — Saturation hull taxonomy (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy
from squarepeg.global_geometry.saturation_hull import audit_saturation_hulls

T116Status = Literal["CONJECTURAL_CLASSIFICATION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T116Certificate:
    status: T116Status
    taxonomy_complete: bool
    curve_level: bool
    messages: list[str]


def certify_t116(tree: CanonicalIntrusionTree) -> T116Certificate:
    hulls = audit_saturation_hulls(tree)
    tax = audit_non_jordan_hull_taxonomy(tree)
    complete = tax.exhaustive and tax.harmless_separated
    status: T116Status = "PROVED_LOCALLY" if complete and hulls.curve_level else "CONJECTURAL_CLASSIFICATION_TARGET"
    return T116Certificate(status, complete, hulls.curve_level, tax.messages)
