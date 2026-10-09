"""T128 — Finite-center route from infinite-center limits (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.center_finite_reduction import audit_center_finite_reduction

T128Status = Literal["CONJECTURAL_ROUTE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T128Certificate:
    status: T128Status
    routed: bool
    obstruction_preserved: bool
    messages: list[str]


def certify_t128(tree: CanonicalIntrusionTree) -> T128Certificate:
    audit = audit_center_finite_reduction(tree)
    status: T128Status = "PROVED_LOCALLY" if audit.all_handled else "CONJECTURAL_ROUTE_TARGET"
    obs = all(r.preserves_obstruction for r in audit.records)
    return T128Certificate(status, audit.all_handled, obs, audit.messages)
