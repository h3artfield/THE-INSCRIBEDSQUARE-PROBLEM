"""T126 — Infinite-center limit decomposition (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.center_accumulation_taxonomy import audit_center_accumulation_taxonomy
from squarepeg.global_geometry.infinite_center_limits import audit_infinite_center_limits

T126Status = Literal["CONJECTURAL_DECOMPOSITION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T126Certificate:
    status: T126Status
    decomposed: bool
    curve_level: bool
    messages: list[str]


def certify_t126(tree: CanonicalIntrusionTree) -> T126Certificate:
    limits = audit_infinite_center_limits(tree)
    tax = audit_center_accumulation_taxonomy(tree)
    decomposed = tax.exhaustive and limits.curve_level
    status: T126Status = "PROVED_LOCALLY" if decomposed else "CONJECTURAL_DECOMPOSITION_TARGET"
    return T126Certificate(status, decomposed, limits.curve_level, tax.messages)
