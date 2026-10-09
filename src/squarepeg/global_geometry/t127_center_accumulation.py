"""T127 — Center accumulation classification (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.center_accumulation_taxonomy import audit_center_accumulation_taxonomy

T127Status = Literal["CONJECTURAL_CLASSIFICATION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T127Certificate:
    status: T127Status
    classified: bool
    messages: list[str]


def certify_t127(tree: CanonicalIntrusionTree) -> T127Certificate:
    tax = audit_center_accumulation_taxonomy(tree)
    status: T127Status = "PROVED_LOCALLY" if tax.exhaustive else "CONJECTURAL_CLASSIFICATION_TARGET"
    return T127Certificate(status, tax.exhaustive, tax.messages)
