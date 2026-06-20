"""Exact routing predicates for augmented transitions (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_order_transition import audit_augmented_order_transition
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.defect_extraction.gate_order_realizability import audit_gate_order_realizability
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure

AugmentedRoute = Literal[
    "R_SUMMABLE_CHILD",
    "R_ORDERED_GATE",
    "R_FINITE_WIDTH_ORDER",
    "R_COUNTABLE_ORDER",
    "R_CONCENTRATION",
    "R_FINITE_CENTER",
    "R_INFINITE_CENTER",
    "R_INFINITE_TREE",
    "R_PARAMETER_DISCONNECTED",
    "R_COLLISION_DEGENERATION",
    "R_POSITIVE_SCALE",
    "UNROUTED",
]

RouteDestination = Literal[
    "T081I",
    "T068I",
    "T073",
    "T073I",
    "T064",
    "T062",
    "INFINITE_CENTER_TRANSITION",
    "T080",
    "PARAMETER_DISCONNECTED_LIMIT",
    "NON_JORDAN_SATURATION_HULL",
    "T091",
    "NONE",
]

ROUTE_DESTINATION: dict[AugmentedRoute, RouteDestination] = {
    "R_SUMMABLE_CHILD": "T081I",
    "R_ORDERED_GATE": "T068I",
    "R_FINITE_WIDTH_ORDER": "T073",
    "R_COUNTABLE_ORDER": "T073I",
    "R_CONCENTRATION": "T064",
    "R_FINITE_CENTER": "T062",
    "R_INFINITE_CENTER": "INFINITE_CENTER_TRANSITION",
    "R_INFINITE_TREE": "T080",
    "R_PARAMETER_DISCONNECTED": "PARAMETER_DISCONNECTED_LIMIT",
    "R_COLLISION_DEGENERATION": "NON_JORDAN_SATURATION_HULL",
    "R_POSITIVE_SCALE": "T091",
    "UNROUTED": "NONE",
}


@dataclass
class AugmentedRouteRecord:
    parent_id: str
    route: AugmentedRoute
    destination: RouteDestination
    realizability: str


@dataclass
class AugmentedTransitionRouteAudit:
    records: list[AugmentedRouteRecord]
    all_routed: bool
    algebraic_excluded: bool
    messages: list[str]


def _assign_route(
    parent_id: str,
    child_moment: float,
    child_count: int,
    cross_area: float,
    diag_mass: float,
    gate_count: int,
    mu_plus: bool,
    depth: int,
    realizable: bool,
) -> AugmentedRoute:
    if not realizable:
        return "UNROUTED"
    if mu_plus or child_moment > 0.9:
        return "R_POSITIVE_SCALE"
    if diag_mass > 0.05 and cross_area > 0.1:
        return "R_COLLISION_DEGENERATION"
    if child_moment < 0.05:
        return "R_CONCENTRATION"
    if child_count > 8 and child_moment > 0.5:
        return "R_INFINITE_CENTER"
    if depth > 6:
        return "R_INFINITE_TREE"
    if child_count > 4 and child_moment < 0.2:
        return "R_FINITE_CENTER"
    if gate_count > 6 and cross_area > 0.5:
        return "R_COUNTABLE_ORDER"
    if gate_count > 3:
        return "R_FINITE_WIDTH_ORDER"
    if cross_area > 0.01:
        return "R_ORDERED_GATE"
    if child_moment < 0.3:
        return "R_SUMMABLE_CHILD"
    return "R_POSITIVE_SCALE"


def audit_augmented_transition_routes(tree: CanonicalIntrusionTree) -> AugmentedTransitionRouteAudit:
    aug = audit_augmented_order_transition(tree)
    child = audit_child_transition_measure(tree)
    pi = audit_marked_gate_measure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    lam = audit_gate_collision_measure(tree)
    real = audit_gate_order_realizability(tree)
    t091 = certify_t091(tree)
    cmap = {m.parent_id: m for m in child.measures}
    pmap = {m.parent_id: m for m in pi.measures}
    omap = {m.parent_id: m for m in omega.measures}
    lmap = {m.parent_id: m for m in lam.measures}
    rmap = {r.parent_id: r.class_ for r in real.records}
    records: list[AugmentedRouteRecord] = []
    for t in aug.transitions:
        nid = t.parent_id
        node = tree.nodes.get(nid)
        cm = cmap.get(nid)
        cc = len(cm.atoms) if cm else 0
        fm = cm.first_moment if cm else 0.0
        gc = len(pmap[nid].atoms) if nid in pmap else 0
        cross = omap[nid].cross_area if nid in omap else 0.0
        diag = lmap[nid].diagonal_mass if nid in lmap else 0.0
        depth = tree.depth if node else 0
        rc = rmap.get(nid, "ALGEBRAIC_ONLY")
        realizable = rc != "ALGEBRAIC_ONLY"
        route = _assign_route(nid, fm, cc, cross, diag, gc, t091.mu_plus_positive, depth, realizable)
        records.append(
            AugmentedRouteRecord(nid, route, ROUTE_DESTINATION[route], rc)
        )
    all_r = all(r.route != "UNROUTED" for r in records) and bool(records)
    alg_ex = all(r.realizability != "ALGEBRAIC_ONLY" for r in records)
    return AugmentedTransitionRouteAudit(
        records=records,
        all_routed=all_r and alg_ex,
        algebraic_excluded=alg_ex,
        messages=[f"n={len(records)}, routed={all_r}"],
    )
