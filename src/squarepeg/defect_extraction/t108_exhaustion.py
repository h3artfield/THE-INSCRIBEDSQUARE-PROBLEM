"""T108 — Order-augmented infinite transition exhaustion (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_transition_routes import audit_augmented_transition_routes
from squarepeg.defect_extraction.augmented_order_classification import audit_augmented_order_classification
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.collision_exhaustion import audit_collision_exhaustion
from squarepeg.defect_extraction.countable_child_transition_routes import certify_t104
from squarepeg.defect_extraction.diffuse_order_transition import audit_diffuse_order_transition
from squarepeg.defect_extraction.pair_interaction_concentration import audit_pair_interaction_concentration
from squarepeg.defect_extraction.t105r_measure_closure import certify_t105r
from squarepeg.defect_extraction.transition_boundary_cases import audit_transition_boundary_cases
from squarepeg.defect_extraction.unbounded_gate_transition_routes import certify_t106

T108Status = Literal["CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T108Certificate:
    status: T108Status
    all_routed: bool
    boundaries_covered: bool
    pair_exhausted: bool
    collision_exhausted: bool
    order_exhausted: bool
    t104_revalidated: bool
    t106_revalidated: bool
    residual_empty: bool
    messages: list[str]


def audit_t108_exhaustion(tree: CanonicalIntrusionTree) -> T108Certificate:
    routes = audit_augmented_transition_routes(tree)
    pair = audit_pair_interaction_concentration(tree)
    collision = audit_collision_exhaustion(tree)
    order = audit_augmented_order_classification(tree)
    diffuse = audit_diffuse_order_transition(tree)
    bounds = audit_transition_boundary_cases(tree)
    t104 = certify_t104(tree)
    t106 = certify_t106(tree)
    t105r = certify_t105r(tree)
    residual_empty = (
        routes.all_routed
        and pair.all_routed
        and collision.all_classified
        and order.all_routed
        and diffuse.all_routed
        and bounds.all_covered
        and t105r.status == "PROVED_LOCALLY"
    )
    status: T108Status = "PROVED_LOCALLY" if residual_empty else "CONJECTURAL_EXHAUSTION_TARGET"
    return T108Certificate(
        status=status,
        all_routed=routes.all_routed,
        boundaries_covered=bounds.all_covered,
        pair_exhausted=pair.all_routed,
        collision_exhausted=collision.all_classified,
        order_exhausted=order.all_routed and diffuse.all_routed,
        t104_revalidated=t104.status == "PROVED_LOCALLY",
        t106_revalidated=t106.status == "PROVED_LOCALLY",
        residual_empty=residual_empty,
        messages=[
            f"routes={routes.all_routed}, pair={pair.all_routed}, "
            f"collision={collision.all_classified}, residual_empty={residual_empty}",
        ],
    )


def certify_t108(tree: CanonicalIntrusionTree) -> T108Certificate:
    return audit_t108_exhaustion(tree)
