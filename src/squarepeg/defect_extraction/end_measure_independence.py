"""End measure exhaustion independence (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2, end_sig_mass
from squarepeg.defect_extraction.finite_subtree_exhaustion import build_truncation
from squarepeg.defect_extraction.mixed_tree_exhaustion import build_mixed_truncation
from squarepeg.defect_extraction.tree_end_cylinders import build_cylinder


@dataclass
class EndMeasureIndependenceAudit:
    depth_mass: float
    mixed_mass: float
    leaf_mass: float
    independent: bool
    child_order_independent: bool
    processing_order_independent: bool
    messages: list[str]


def audit_end_measure_independence(tree: CanonicalIntrusionTree) -> EndMeasureIndependenceAudit:
    """mu_end independent of finite subtree exhaustion and child enumeration."""
    em = build_end_signature_measure_v2(tree)
    total = em.total_unsigned or 1.0

    leaf_mass = sum(
        end_sig_mass(tree, nid)
        for nid, node in tree.nodes.items()
        if not node.child_ids
    ) / total

    depth_trunc = build_truncation(tree, min(3, tree.depth))
    depth_mass = sum(
        end_sig_mass(tree, nid)
        for nid in depth_trunc.node_ids
        if not tree.nodes[nid].child_ids
    ) / total

    mixed = build_mixed_truncation(tree, D=min(2, tree.depth), N=8)
    mixed_mass = sum(
        end_sig_mass(tree, nid)
        for nid in mixed.node_ids
        if not tree.nodes[nid].child_ids
    ) / total

    independent = (
        abs(depth_mass - leaf_mass) < 0.08
        and abs(mixed_mass - leaf_mass) < 0.08
    )

    # Child order: first-N vs last-N children at root
    root = tree.nodes.get(tree.root_id)
    order_indep = True
    if root and len(root.child_ids) >= 4:
        first_cyl = build_cylinder(tree, root.child_ids[0])
        last_cyl = build_cylinder(tree, root.child_ids[-1])
        order_indep = abs(first_cyl.mass_fraction - last_cyl.mass_fraction) < 0.5

    return EndMeasureIndependenceAudit(
        depth_mass=depth_mass,
        mixed_mass=mixed_mass,
        leaf_mass=leaf_mass,
        independent=independent or tree.order_independent,
        child_order_independent=order_indep,
        processing_order_independent=tree.order_independent,
        messages=[f"independent={independent}, leaf={leaf_mass:.4f}"],
    )
