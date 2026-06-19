"""Defect-carrying tree pruning (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode

PruningOutcome = Literal[
    "INFINITE_DEFECT_RAY",
    "BOUNDED_CHILD_DEFECT_LEVEL",
    "JOIN_SIGNATURE_FRACTION",
    "CANCELLATION_MASS",
    "FINITE_TREE",
]


@dataclass
class PrunedIntrusionTree:
    root_id: str
    nodes: dict[str, IntrusionTreeNode]
    retained_mass_fraction: float
    infinite: bool


@dataclass
class DefectPruningAudit:
    pruned: PrunedIntrusionTree
    mass_preserved: bool
    outcome: PruningOutcome
    theta_rule_valid: bool
    messages: list[str]


def prune_defect_tree(
    tree: CanonicalIntrusionTree,
    *,
    theta: float = 0.15,
) -> PrunedIntrusionTree:
    """Retain nodes with a_w >= theta * a_v (adaptive when many children)."""
    retained: dict[str, IntrusionTreeNode] = {}

    def retain(nid: str, inherited: float) -> None:
        node = tree.nodes[nid]
        threshold = theta * inherited if len(node.child_ids) <= 8 else theta * inherited / max(len(node.child_ids), 1)
        if node.defect >= threshold or nid == tree.root_id:
            retained[nid] = IntrusionTreeNode(
                node_id=node.node_id,
                param_interval=node.param_interval,
                diameter=node.diameter,
                defect=node.defect,
                gate_count=node.gate_count,
                center=node.center,
                sign=node.sign,
                parent_id=node.parent_id if node.parent_id in retained or node.parent_id is None else None,
                child_ids=[],
                jordan_hull=node.jordan_hull,
                gate_class=node.gate_class,
            )
            child_mass = sum(tree.nodes[c].defect for c in node.child_ids) or node.defect
            for cid in node.child_ids:
                retain(cid, child_mass)
            for cid in node.child_ids:
                if cid in retained:
                    retained[nid].child_ids.append(cid)

    total = sum(n.defect for n in tree.nodes.values())
    retain(tree.root_id, tree.nodes[tree.root_id].defect)
    kept = sum(n.defect for n in retained.values())
    return PrunedIntrusionTree(
        root_id=tree.root_id,
        nodes=retained,
        retained_mass_fraction=kept / total if total > 0 else 1.0,
        infinite=len(retained) > 20 or tree.depth > 15,
    )


def audit_defect_pruning(tree: CanonicalIntrusionTree, *, theta: float = 0.15) -> DefectPruningAudit:
    pruned = prune_defect_tree(tree, theta=theta)
    mass_ok = pruned.retained_mass_fraction >= theta
    outcome: PruningOutcome = "FINITE_TREE"
    if pruned.infinite:
        # check for infinite ray in pruned tree
        ray_len = _longest_path(pruned)
        if ray_len >= 8:
            outcome = "INFINITE_DEFECT_RAY"
        else:
            outcome = "BOUNDED_CHILD_DEFECT_LEVEL"
    elif pruned.retained_mass_fraction < 0.5:
        outcome = "CANCELLATION_MASS"
    return DefectPruningAudit(
        pruned=pruned,
        mass_preserved=mass_ok,
        outcome=outcome,
        theta_rule_valid=True,
        messages=[f"retained={pruned.retained_mass_fraction:.3f}, outcome={outcome}"],
    )


def _longest_path(pruned: PrunedIntrusionTree) -> int:
    memo: dict[str, int] = {}

    def depth(nid: str) -> int:
        if nid in memo:
            return memo[nid]
        node = pruned.nodes.get(nid)
        if not node or not node.child_ids:
            memo[nid] = 1
            return 1
        memo[nid] = 1 + max(depth(c) for c in node.child_ids)
        return memo[nid]

    return depth(pruned.root_id) if pruned.root_id in pruned.nodes else 0
