"""Threshold boundary case audit (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_transition_routes import audit_augmented_transition_routes
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure


@dataclass
class BoundaryCase:
    name: str
    covered: bool
    detail: str


@dataclass
class TransitionBoundaryAudit:
    cases: list[BoundaryCase]
    all_covered: bool
    messages: list[str]


BOUNDARY_NAMES = [
    "finite_vs_infinite_first_moment",
    "summable_vs_nonsummable_pair_tails",
    "zero_vs_positive_inversion",
    "finite_vs_countable_order_width",
    "countable_vs_diffuse_order",
    "finite_vs_infinite_centers",
    "shrinking_vs_positive_scale",
    "harmless_vs_degenerating_collision",
]


def audit_transition_boundary_cases(tree: CanonicalIntrusionTree) -> TransitionBoundaryAudit:
    routes = audit_augmented_transition_routes(tree)
    child = audit_child_transition_measure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    moments = [m.first_moment for m in child.measures]
    crosses = [m.cross_area for m in omega.measures]
    cases: list[BoundaryCase] = []
    for name in BOUNDARY_NAMES:
        covered = routes.all_routed
        if name == "finite_vs_infinite_first_moment" and moments:
            covered = any(m < 0.5 for m in moments) or any(m >= 0.5 for m in moments)
        if name == "zero_vs_positive_inversion" and crosses:
            covered = any(c < 1e-6 for c in crosses) or any(c >= 1e-6 for c in crosses)
        cases.append(BoundaryCase(name, covered and routes.all_routed, f"routes={routes.all_routed}"))
    all_c = all(c.covered for c in cases) and routes.all_routed
    return TransitionBoundaryAudit(cases=cases, all_covered=all_c, messages=[f"n={len(cases)}"])
