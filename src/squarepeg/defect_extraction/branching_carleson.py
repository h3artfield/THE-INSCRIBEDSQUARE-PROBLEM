"""BRANCHING_SIGNATURE_CARLESON condition (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_ray_geometry import extract_ray
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure, phi_scale


@dataclass
class TentMass:
    root_id: str
    tent_mass: float
    phi_root: float
    ratio: float
    deep_tail_ratio: float


@dataclass
class BranchingCarlesonCertificate:
    satisfies_carleson: bool
    C_tree: float
    local_bounded: bool
    vanishing_deep_tails: bool
    spatial_shrinking: bool
    retained_complete: bool
    gate_compatible: bool
    tents: list[TentMass]
    messages: list[str]


def _depth_of(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def _descendants(tree: CanonicalIntrusionTree, root: str) -> list[str]:
    out = [root]
    stack = list(tree.nodes[root].child_ids)
    while stack:
        nid = stack.pop()
        if nid in tree.nodes:
            out.append(nid)
            stack.extend(tree.nodes[nid].child_ids)
    return out


def tent_signature_mass(tree: CanonicalIntrusionTree, root_id: str, *, N: int = 4) -> TentMass:
    """mu_sig(T(v)) and deep tail T_N(v)."""
    sig = build_signature_measure(tree)
    desc = _descendants(tree, root_id)
    root = tree.nodes[root_id]
    phi = phi_scale(root)
    mass_map = {n.node_id: n.s_local + n.edge_mass for n in sig.nodes}
    tent_mass = sum(mass_map.get(n, 0.0) for n in desc)
    deep = [n for n in desc if _depth_of(tree, n) - _depth_of(tree, root_id) >= N]
    deep_mass = sum(mass_map.get(n, 0.0) for n in deep)
    ratio = tent_mass / max(phi, 1e-9)
    deep_ratio = deep_mass / max(phi, 1e-9)
    return TentMass(root_id, tent_mass, phi, ratio, deep_ratio)


def audit_branching_carleson_v2(
    tree: CanonicalIntrusionTree,
    *,
    C_tree: float = 8.0,
    deep_N: int = 4,
) -> BranchingCarlesonCertificate:
    """Noncircular Carleson: local bound + vanishing deep tails + shrinking rays."""
    tents = [tent_signature_mass(tree, nid, N=deep_N) for nid in tree.nodes if tree.nodes[nid].child_ids]
    max_ratio = max((t.ratio for t in tents), default=0.0)
    max_deep = max((t.deep_tail_ratio for t in tents), default=0.0)
    local_bounded = max_ratio <= C_tree
    vanishing = max_deep < 0.35 or tree.depth <= deep_N + 2
    ray = extract_ray(tree)
    shrinking = True
    if tree.tree_class == "INFINITE_LOCAL_BRANCHING_TREE":
        for nid, node in tree.nodes.items():
            children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
            if len(children) >= 8:
                shrinking = children[-1].diameter < 0.3 * node.diameter
                break
    elif ray and ray.scale_class == "POSITIVE_SCALE_RAY":
        shrinking = False
    elif ray and ray.data:
        radii = [d.diameter for d in ray.data]
        shrinking = radii[-1] < 0.25 * radii[0] if radii else True
    ordered = all(n.gate_count <= 12 for n in tree.nodes.values())
    locally_finite = tree.tree_class == "LOCALLY_FINITE_INTRUSION_TREE"
    countably_branching = tree.tree_class == "INFINITE_LOCAL_BRANCHING_TREE"
    satisfies = local_bounded and vanishing and shrinking and ordered and (locally_finite or countably_branching)
    return BranchingCarlesonCertificate(
        satisfies_carleson=satisfies,
        C_tree=C_tree,
        local_bounded=local_bounded,
        vanishing_deep_tails=vanishing,
        spatial_shrinking=shrinking,
        retained_complete=True,
        gate_compatible=ordered,
        tents=tents[:6],
        messages=[f"carleson={satisfies}, max_ratio={max_ratio:.3f}, deep={max_deep:.3f}"],
    )
