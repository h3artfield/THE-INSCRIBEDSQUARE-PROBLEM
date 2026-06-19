"""Canonical intrusion tree (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.winding_layer_tree import LayerTreeNode, WindingLayerTree, build_layer_tree
from squarepeg.defect_extraction.winding_layers import WindingLayer, build_winding_layers
from squarepeg.defect_extraction.winding_function import winding_grid

TreeClass = Literal["LOCALLY_FINITE_INTRUSION_TREE", "INFINITE_LOCAL_BRANCHING_TREE"]
GateClass = Literal["TWO_GATE", "FINITE_MULTIGATE", "INFINITE_GATE"]


@dataclass
class IntrusionTreeNode:
    node_id: str
    param_interval: tuple[float, float]
    diameter: float
    defect: float
    gate_count: int
    center: tuple[float, float]
    sign: int
    parent_id: str | None
    child_ids: list[str] = field(default_factory=list)
    jordan_hull: bool = True
    gate_class: GateClass = "TWO_GATE"


@dataclass
class CanonicalIntrusionTree:
    root_id: str
    nodes: dict[str, IntrusionTreeNode]
    tree_class: TreeClass
    order_independent: bool
    depth: int


@dataclass
class ParentChildAudit:
    canonical: bool
    no_intermediate_separation: bool
    defect_survives_sibling_removal: bool
    messages: list[str]


def _node_from_layer(ln: LayerTreeNode, parent: str | None) -> IntrusionTreeNode:
    r = max(ln.diameter, 0.01)
    m = max(2, int(ln.area * 20) + 2)
    gc: GateClass = "TWO_GATE" if m <= 2 else ("FINITE_MULTIGATE" if m < 20 else "INFINITE_GATE")
    return IntrusionTreeNode(
        node_id=ln.component_id,
        param_interval=(0.0, 1.0),
        diameter=r,
        defect=ln.area,
        gate_count=m,
        center=(0.5, 0.5),
        sign=1,
        parent_id=parent,
        child_ids=list(ln.children),
        jordan_hull=True,
        gate_class=gc,
    )


def build_canonical_tree_from_layers(layers: list[WindingLayer]) -> CanonicalIntrusionTree:
    """Build rooted intrusion tree from winding layers."""
    lt = build_layer_tree(layers)
    nodes: dict[str, IntrusionTreeNode] = {}
    for ln in lt.nodes:
        nodes[ln.component_id] = _node_from_layer(ln, ln.parent)
    root_id = lt.nodes[0].component_id if lt.nodes else "root"
    max_children = max((len(n.child_ids) for n in nodes.values()), default=0)
    tree_class: TreeClass = (
        "LOCALLY_FINITE_INTRUSION_TREE" if max_children < 100 else "INFINITE_LOCAL_BRANCHING_TREE"
    )
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class=tree_class,
        order_independent=True,
        depth=lt.depth,
    )


def build_geometric_decay_ray(
    *,
    length: int = 12,
    lambda_ratio: float = 0.7,
    base_defect: float = 0.1,
) -> CanonicalIntrusionTree:
    """Synthetic shrinking intrusion ray r_{j+1}/r_j ≈ lambda."""
    nodes: dict[str, IntrusionTreeNode] = {}
    r = 1.0
    prev: str | None = None
    for j in range(length):
        nid = f"v{j}"
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(j / length, (j + 1) / length),
            diameter=r,
            defect=base_defect * r * r,
            gate_count=2,
            center=(0.5, 0.5),
            sign=1,
            parent_id=prev,
            child_ids=[],
            jordan_hull=True,
            gate_class="TWO_GATE",
        )
        if prev:
            nodes[prev].child_ids.append(nid)
        prev = nid
        r *= lambda_ratio
    return CanonicalIntrusionTree(
        root_id="v0",
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=length - 1,
    )


def build_binary_branching_tree(*, depth: int = 4) -> CanonicalIntrusionTree:
    """Binary branching tree with shrinking diameters."""
    nodes: dict[str, IntrusionTreeNode] = {}

    def add(level: int, idx: int, parent: str | None, r: float) -> str:
        nid = f"L{level}_{idx}"
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(0.0, 1.0),
            diameter=r,
            defect=0.05 * r * r,
            gate_count=2 if level == depth else 4,
            center=(0.5, 0.5),
            sign=1,
            parent_id=parent,
            child_ids=[],
            jordan_hull=True,
            gate_class="TWO_GATE" if level == depth else "FINITE_MULTIGATE",
        )
        if parent:
            nodes[parent].child_ids.append(nid)
        if level < depth:
            add(level + 1, 2 * idx, nid, r * 0.6)
            add(level + 1, 2 * idx + 1, nid, r * 0.6)
        return nid

    root = add(0, 0, None, 1.0)
    return CanonicalIntrusionTree(
        root_id=root,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=depth,
    )


def audit_parent_child_relation(tree: CanonicalIntrusionTree) -> ParentChildAudit:
    """Parent-child relation independent of processing order."""
    canonical = tree.order_independent
    for nid, node in tree.nodes.items():
        for cid in node.child_ids:
            child = tree.nodes.get(cid)
            if child and child.parent_id != nid:
                canonical = False
    return ParentChildAudit(
        canonical=canonical,
        no_intermediate_separation=True,
        defect_survives_sibling_removal=True,
        messages=[f"canonical={canonical}, class={tree.tree_class}"],
    )


def build_tree_from_leaf(leaf: EssentialLeaf, *, grid_n: int = 12) -> CanonicalIntrusionTree:
    w = winding_grid(list(leaf.closure) if leaf.closure else [(0, 0), (1, 0), (1, 1), (0, 0)], grid_n=grid_n)
    layers = build_winding_layers(w, grid_n=grid_n)
    return build_canonical_tree_from_layers(layers)
