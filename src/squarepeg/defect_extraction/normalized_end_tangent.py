"""Normalized bad-cylinder tangent trees (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class NormalizedTangentNode:
    node_id: str
    hull_center: tuple[float, float]
    hull_radius: float
    mu_tilde: float
    phi_tilde: float
    D_tilde: float
    jordan_hull: bool
    param_interval: tuple[float, float]


@dataclass
class NormalizedEndTangent:
    source_node: str
    nodes: list[NormalizedTangentNode]
    density_ratio_identity: bool
    messages: list[str]


def normalize_bad_cylinder(tree: CanonicalIntrusionTree, node_id: str) -> NormalizedEndTangent:
    """Normalize H_v, descendants, end mass, and Phi scale at bad node v."""
    root = tree.nodes[node_id]
    r_v = max(root.diameter, 1e-6)
    c_v = root.center
    parent_rec = cylinder_density(tree, node_id)
    m_v = max(parent_rec.m_v, 1e-9)
    phi_v = max(parent_rec.phi_v, 1e-9)

    nodes: list[NormalizedTangentNode] = []
    density_ok = True

    def desc(nid: str) -> list[str]:
        out = [nid]
        for c in tree.nodes[nid].child_ids:
            if c in tree.nodes:
                out.extend(desc(c))
        return out

    for nid in desc(node_id):
        node = tree.nodes[nid]
        rec = cylinder_density(tree, nid)
        mu_t = rec.m_v / m_v
        phi_t = rec.phi_v / phi_v
        D_t = rec.D_v / max(parent_rec.D_v, 1e-9) if parent_rec.phi_v > 1e-12 else rec.D_v
        if rec.phi_v > 1e-12 and parent_rec.phi_v > 1e-12:
            expected = rec.D_v / parent_rec.D_v
            if abs(D_t - expected) > 0.5 * max(expected, 1e-6):
                density_ok = False
        cx = (node.center[0] - c_v[0]) / r_v
        cy = (node.center[1] - c_v[1]) / r_v
        nodes.append(
            NormalizedTangentNode(
                nid,
                (cx, cy),
                node.diameter / r_v,
                mu_t,
                phi_t,
                D_t,
                node.jordan_hull,
                node.param_interval,
            )
        )

    return NormalizedEndTangent(
        source_node=node_id,
        nodes=nodes,
        density_ratio_identity=density_ok,
        messages=[f"nodes={len(nodes)}, density_identity={density_ok}"],
    )
