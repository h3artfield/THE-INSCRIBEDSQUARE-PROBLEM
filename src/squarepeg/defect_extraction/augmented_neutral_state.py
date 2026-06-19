"""Augmented neutral state vector X(v) (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.signature_budget import audit_signature_budget

StateClass = Literal[
    "NORMALIZED",
    "ZERO_SIGNATURE_STATE",
    "DEGENERATE_STATE_NORMALIZATION",
    "POSITIVE_SCALE_STATE",
    "NON_JORDAN_STATE",
]


@dataclass
class AugmentedState:
    node_id: str
    Phi: float
    R: float
    S: float
    J: float
    C: float
    B: float
    G: float
    state_class: StateClass
    X_hat: tuple[float, float, float, float, float, float, float]


@dataclass
class AugmentedStateAudit:
    states: list[AugmentedState]
    neutral_count: int
    messages: list[str]


def _sign_grouping(tree: CanonicalIntrusionTree, node_id: str) -> float:
    node = tree.nodes[node_id]
    if len(node.child_ids) < 2:
        return 0.0
    signs = []
    for cid in node.child_ids:
        if cid not in tree.nodes:
            continue
        c = tree.nodes[cid]
        signs.append(1.0 if c.center[0] >= node.center[0] else -1.0)
    return abs(sum(signs)) / max(len(signs), 1)


def _gate_complexity(tree: CanonicalIntrusionTree, node_id: str) -> float:
    node = tree.nodes[node_id]
    return float(node.gate_count) * node.diameter


def compute_state(
    tree: CanonicalIntrusionTree,
    node_id: str,
    *,
    budget_map: dict | None = None,
) -> AugmentedState:
    rec = cylinder_density(tree, node_id)
    br = budget_map.get(node_id) if budget_map else None
    if br is None:
        budget = audit_signature_budget(tree)
        budget_map = {b.node_id: b for b in budget.records}
        br = budget_map.get(node_id)
    phi = rec.phi_v
    R = br.retained_skeleton if br else 0.0
    J = (br.wedge_child_child + br.wedge_parent_child) if br else 0.0
    C = br.crosscut_area if br else 0.0
    S = _sign_grouping(tree, node_id) * phi * 0.1
    B = 0.05 * phi
    G = _gate_complexity(tree, node_id)
    sc: StateClass = "NORMALIZED"
    if phi <= 1e-12:
        sc = "ZERO_SIGNATURE_STATE"
    inv = 1.0 / phi if phi > 1e-12 else 0.0
    X_hat = (1.0, R * inv, S * inv, J * inv, C * inv, B * inv, G * inv)
    return AugmentedState(node_id, phi, R, S, J, C, B, G, sc, X_hat)


def audit_augmented_neutral_state(tree: CanonicalIntrusionTree) -> AugmentedStateAudit:
    corona = audit_cantor_corona(tree)
    neutral = {c.node_id for c in corona.classifications if c.node_class == "NEUTRAL"}
    for nid in list(neutral):
        if nid not in tree.nodes:
            continue
        for cid in tree.nodes[nid].child_ids:
            if cid in tree.nodes:
                neutral.add(cid)
    budget = audit_signature_budget(tree)
    budget_map = {b.node_id: b for b in budget.records}
    states: list[AugmentedState] = []
    seen: set[str] = set()
    for nid in neutral:
        if nid in tree.nodes and tree.nodes[nid].child_ids and nid not in seen:
            seen.add(nid)
            states.append(compute_state(tree, nid, budget_map=budget_map))
        elif nid in tree.nodes and nid not in seen:
            seen.add(nid)
            states.append(compute_state(tree, nid, budget_map=budget_map))
    return AugmentedStateAudit(
        states=states,
        neutral_count=len(states),
        messages=[f"neutral_states={len(states)}"],
    )
