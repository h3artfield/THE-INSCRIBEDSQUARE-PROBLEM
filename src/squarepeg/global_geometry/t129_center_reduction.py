"""T129 — Infinite-center to parameter/diffuse reduction (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.center_to_diffuse_end_routes import audit_center_to_diffuse_end_routes
from squarepeg.global_geometry.center_to_parameter_routes import audit_center_to_parameter_routes

T129Status = Literal["CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T129Certificate:
    status: T129Status
    reduced: bool
    messages: list[str]


def certify_t129(tree: CanonicalIntrusionTree) -> T129Certificate:
    param = audit_center_to_parameter_routes(tree)
    diffuse = audit_center_to_diffuse_end_routes(tree)
    reduced = param.distinct_from_diffuse and diffuse.distinct_from_parameter
    status: T129Status = "PROVED_LOCALLY" if reduced else "CONJECTURAL_REDUCTION_TARGET"
    return T129Certificate(status, reduced, [f"param={param.distinct_from_diffuse}"])
