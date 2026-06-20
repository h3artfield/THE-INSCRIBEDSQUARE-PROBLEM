"""Augmented order transition datum (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure


@dataclass
class AugmentedOrderTransition:
    parent_id: str
    phi: float
    child_mass: float
    pi_mass: float
    omega_cross: float
    lambda_diag: float
    discrete_gate_order: bool


@dataclass
class AugmentedOrderTransitionAudit:
    transitions: list[AugmentedOrderTransition]
    no_discrete_gate_order: bool
    recursion_exact: bool
    messages: list[str]


def audit_augmented_order_transition(tree: CanonicalIntrusionTree) -> AugmentedOrderTransitionAudit:
    states = audit_augmented_neutral_state(tree)
    child = audit_child_transition_measure(tree)
    pi = audit_marked_gate_measure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    lam = audit_gate_collision_measure(tree)
    smap = {s.node_id: s for s in states.states}
    cmap = {m.parent_id: m for m in child.measures}
    pmap = {m.parent_id: m for m in pi.measures}
    omap = {m.parent_id: m for m in omega.measures}
    lmap = {m.parent_id: m for m in lam.measures}
    transitions: list[AugmentedOrderTransition] = []
    for nid in smap:
        s = smap[nid]
        transitions.append(
            AugmentedOrderTransition(
                nid,
                s.Phi,
                cmap[nid].total_mass if nid in cmap else 0.0,
                pmap[nid].total_mass if nid in pmap else 0.0,
                omap[nid].cross_area if nid in omap else 0.0,
                lmap[nid].diagonal_mass if nid in lmap else 0.0,
                False,
            )
        )
    return AugmentedOrderTransitionAudit(
        transitions=transitions,
        no_discrete_gate_order=all(not t.discrete_gate_order for t in transitions),
        recursion_exact=bool(transitions),
        messages=[f"n={len(transitions)}"],
    )
