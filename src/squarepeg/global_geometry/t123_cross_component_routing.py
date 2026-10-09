"""T123 — Cross-component interaction routing (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.cross_component_interactions import audit_cross_component_interactions

T123Status = Literal["CONJECTURAL_INTERACTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T123Certificate:
    status: T123Status
    routed: bool
    interactions_retained: bool
    messages: list[str]


def certify_t123(tree: CanonicalIntrusionTree) -> T123Certificate:
    audit = audit_cross_component_interactions(tree)
    status: T123Status = "PROVED_LOCALLY" if audit.all_routed and audit.never_discarded else "CONJECTURAL_INTERACTION_TARGET"
    return T123Certificate(status, audit.all_routed, audit.never_discarded, audit.messages)
