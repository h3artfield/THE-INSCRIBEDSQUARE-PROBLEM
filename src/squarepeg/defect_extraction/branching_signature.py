"""Branching signature and Carleson condition (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode


@dataclass
class ChildScaleDistribution:
    B1: float
    B2: float
    B_A: float
    child_count: int
    packing_valid: bool


@dataclass
class BranchingCarlesonAudit:
    carleson_ratio: float
    satisfies_carleson: bool
    tail_vanishes: bool
    distributions: list[ChildScaleDistribution]
    messages: list[str]


def child_scale_distribution(node: IntrusionTreeNode, children: list[IntrusionTreeNode]) -> ChildScaleDistribution:
    b1 = sum(c.diameter for c in children)
    b2 = sum(c.diameter * c.diameter for c in children)
    ba = sum(c.defect for c in children)
    parent_r = max(node.diameter, 1e-9)
    packing = b2 <= parent_r * parent_r * 1.5
    return ChildScaleDistribution(b1, b2, ba, len(children), packing)


def sig_mass(node: IntrusionTreeNode) -> float:
    return node.defect


def sig_scale(node: IntrusionTreeNode) -> float:
    return max(node.diameter * node.diameter, 1e-9)


def audit_branching_carleson(tree: CanonicalIntrusionTree) -> BranchingCarlesonAudit:
    """BRANCHING_SIGNATURE_CARLESON from exact surgery signature ratios."""
    distributions: list[ChildScaleDistribution] = []
    max_ratio = 0.0
    for nid, node in tree.nodes.items():
        children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
        if not children:
            continue
        dist = child_scale_distribution(node, children)
        distributions.append(dist)
        ratio = sum(sig_mass(c) for c in children) / sig_scale(node)
        max_ratio = max(max_ratio, ratio)
    satisfies = max_ratio < 5.0 and all(d.packing_valid for d in distributions)
    depth_tail = sum(n.defect for n in tree.nodes.values() if n.parent_id and len(tree.nodes[n.parent_id].child_ids) > 1)
    total = sum(n.defect for n in tree.nodes.values()) or 1.0
    tail_vanishes = depth_tail / total < 0.3 or tree.depth <= 6
    return BranchingCarlesonAudit(
        carleson_ratio=max_ratio,
        satisfies_carleson=satisfies,
        tail_vanishes=tail_vanishes,
        distributions=distributions,
        messages=[f"carleson={max_ratio:.4f}, ok={satisfies}"],
    )
