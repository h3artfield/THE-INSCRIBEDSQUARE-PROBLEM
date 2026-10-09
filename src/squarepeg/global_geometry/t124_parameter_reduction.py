"""T124 — Parameter-disconnected to center/diffuse reduction (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.cantor_parameter_support import audit_cantor_parameter_support
from squarepeg.global_geometry.countable_component_parameter_split import audit_countable_component_parameter_split
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits
from squarepeg.global_geometry.parameter_to_center_routes import audit_parameter_to_center_routes
from squarepeg.global_geometry.parameter_to_diffuse_end_routes import audit_parameter_to_diffuse_end_routes

T124Status = Literal["CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T124Certificate:
    status: T124Status
    reduced: bool
    messages: list[str]


def certify_t124(tree: CanonicalIntrusionTree) -> T124Certificate:
    limits = audit_parameter_disconnected_limits(tree)
    countable = audit_countable_component_parameter_split(tree)
    cantor = audit_cantor_parameter_support(tree)
    center = audit_parameter_to_center_routes(tree)
    diffuse = audit_parameter_to_diffuse_end_routes(tree)
    true_disc = any(r.true_disconnection for r in limits.records)
    reduced = (
        cantor.no_singleton_cantor_reintroduced
        and center.distinct_from_diffuse
        and diffuse.distinct_from_center
        and countable.all_classified
    )
    if not true_disc:
        reduced = True
    status: T124Status = "PROVED_LOCALLY" if reduced else "CONJECTURAL_REDUCTION_TARGET"
    return T124Certificate(status, reduced, [f"true_disc={true_disc}"])
