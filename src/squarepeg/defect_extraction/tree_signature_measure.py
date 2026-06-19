"""Tree signature measure derived from wedge identity (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode
from squarepeg.defect_extraction.tree_attachment_identity import child_join_term


@dataclass
class NodeSignature:
    node_id: str
    s_local: float
    s_total: float
    phi_scale: float
    edge_mass: float


@dataclass
class TreeSignatureMeasure:
    nodes: list[NodeSignature]
    total_mass: float
    edge_total: float
    derived_from_wedge: bool


def phi_scale(node: IntrusionTreeNode) -> float:
    """Parent-scale quantity Phi(v) = M_v^2 r_v^2."""
    return float(node.gate_count ** 2 * node.diameter ** 2)


def edge_weight(parent: IntrusionTreeNode, child: IntrusionTreeNode, *, C: float = 1.0) -> float:
    """e(v,w) <= C M_v M_w r_v r_w."""
    return C * parent.gate_count * child.gate_count * parent.diameter * child.diameter


def node_signature_weight(
    node: IntrusionTreeNode,
    children: list[IntrusionTreeNode],
) -> float:
    """s(v) from wedge: local + child joins + recursive tail (finite trees)."""
    local = phi_scale(node)
    join = child_join_term(node, children).join_area if children else 0.0
    child_rw = sum(c.gate_count * c.diameter for c in children)
    parent_term = node.diameter * child_rw
    return local + join + parent_term


def build_signature_measure(tree: CanonicalIntrusionTree) -> TreeSignatureMeasure:
    """mu_sig = sum s_local(v) delta_v + sum e(v,w) delta_{(v,w)}."""
    nodes: list[NodeSignature] = []
    edge_total = 0.0

    def total_s(nid: str) -> float:
        node = tree.nodes[nid]
        children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
        base = node_signature_weight(node, children)
        for c in children:
            base += total_s(c.node_id) * 0.0  # children counted via join terms at parent
        return base

    for nid, node in tree.nodes.items():
        children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
        s_loc = node_signature_weight(node, children)
        e_mass = sum(edge_weight(node, c) for c in children)
        edge_total += e_mass
        nodes.append(
            NodeSignature(
                node_id=nid,
                s_local=s_loc,
                s_total=total_s(nid),
                phi_scale=phi_scale(node),
                edge_mass=e_mass,
            )
        )
    total = sum(n.s_local for n in nodes) + edge_total
    return TreeSignatureMeasure(
        nodes=nodes,
        total_mass=total,
        edge_total=edge_total,
        derived_from_wedge=True,
    )
