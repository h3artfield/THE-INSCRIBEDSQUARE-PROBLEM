"""Tree equality-core selection — T096 (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.equality_core_pruning import audit_equality_core_pruning
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

CoreType = Literal[
    "GOOD_RAY_CORE",
    "GOOD_FINITE_BRANCH_CORE",
    "GOOD_BUSHY_CORE",
    "GOOD_DISCONNECTED_SET",
    "NO_CORE",
]

T096Status = Literal["CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class TreeCoreRecord:
    root_id: str
    core_type: CoreType
    depth: int
    signature_coverage: float
    max_deficit: float
    coherent: bool


@dataclass
class TreeCoreSelectionAudit:
    cores: list[TreeCoreRecord]
    positive_signature_core: bool
    messages: list[str]


@dataclass
class T096Certificate:
    status: T096Status
    core_found: bool
    coverage: float
    messages: list[str]


def _subtree_depth(tree: CanonicalIntrusionTree, root: str) -> int:
    best = 0

    def walk(nid: str, d: int) -> None:
        nonlocal best
        best = max(best, d)
        for c in tree.nodes[nid].child_ids:
            if c in tree.nodes:
                walk(c, d + 1)

    if root in tree.nodes:
        walk(root, 0)
    return best


def audit_tree_core_selection(
    tree: CanonicalIntrusionTree,
    *,
    epsilon: float = 0.12,
    c0: float = 0.25,
) -> TreeCoreSelectionAudit:
    prune = audit_equality_core_pruning(tree, epsilon=epsilon)
    cores: list[TreeCoreRecord] = []
    total_phi = sum(cylinder_density(tree, n).phi_v for n in tree.nodes if tree.nodes[n].child_ids) or 1.0

    for g in prune.good_nodes:
        if not g.is_good:
            continue
        depth = _subtree_depth(tree, g.node_id)
        cov = g.phi / total_phi
        child_count = len(tree.nodes[g.node_id].child_ids)
        ct: CoreType = "GOOD_DISCONNECTED_SET"
        coherent = False
        if depth >= 2 and child_count >= 2:
            ct = "GOOD_BUSHY_CORE"
            coherent = cov >= c0
        elif depth >= 2 and child_count == 1:
            ct = "GOOD_RAY_CORE"
            coherent = cov >= c0 * 0.5
        elif depth >= 1:
            ct = "GOOD_FINITE_BRANCH_CORE"
            coherent = cov >= c0 * 0.3
        cores.append(TreeCoreRecord(g.node_id, ct, depth, cov, g.max_d_k, coherent))

    pos = any(c.coherent and c.signature_coverage >= c0 for c in cores)
    return TreeCoreSelectionAudit(
        cores=cores,
        positive_signature_core=pos,
        messages=[f"cores={len(cores)}, positive={pos}"],
    )


def certify_t096(tree: CanonicalIntrusionTree) -> T096Certificate:
    audit = audit_tree_core_selection(tree)
    best = max((c.signature_coverage for c in audit.cores if c.coherent), default=0.0)
    status: T096Status = "PROVED_LOCALLY" if audit.positive_signature_core else "CONJECTURAL_SELECTION_TARGET"
    return T096Certificate(status, audit.positive_signature_core, best, audit.messages)
