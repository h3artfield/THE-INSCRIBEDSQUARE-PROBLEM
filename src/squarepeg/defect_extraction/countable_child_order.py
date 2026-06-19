"""Canonical countable child ordering (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import (
    CanonicalIntrusionTree,
    IntrusionTreeNode,
    TreeClass,
)

ChildAccumulation = Literal[
    "SINGLE_POINT_CHILD_ACCUMULATION",
    "FINITE_CENTER_CHILD_ACCUMULATION",
    "DIFFUSE_CHILD_CENTER_DISTRIBUTION",
    "PARAMETER_ENDPOINT_ACCUMULATION",
    "POSITIVE_SCALE_CHILDREN",
    "NON_JORDAN_CHILD_ACCUMULATION",
]


@dataclass
class CountableChildRecord:
    child_id: str
    index: int
    diameter: float
    gate_count: int
    defect: float
    delta_norm: float
    center: tuple[float, float]
    param_interval: tuple[float, float]
    sign: int


@dataclass
class CountableChildFamily:
    parent_id: str
    children: list[CountableChildRecord]
    canonical_order: bool
    accumulation_labels: list[ChildAccumulation]


def delta_increment(child: IntrusionTreeNode) -> float:
    """|Delta_{w_i}| from actual attachment increment."""
    return child.diameter * child.gate_count * 0.1


def canonical_child_order(
    parent: IntrusionTreeNode,
    children: list[IntrusionTreeNode],
) -> list[CountableChildRecord]:
    """Deterministic order by parameter interval start."""
    ordered = sorted(children, key=lambda c: c.param_interval[0])
    return [
        CountableChildRecord(
            child_id=c.node_id,
            index=i,
            diameter=c.diameter,
            gate_count=c.gate_count,
            defect=c.defect,
            delta_norm=delta_increment(c),
            center=c.center,
            param_interval=c.param_interval,
            sign=c.sign,
        )
        for i, c in enumerate(ordered)
    ]


def classify_child_accumulation(records: list[CountableChildRecord]) -> list[ChildAccumulation]:
    labels: list[ChildAccumulation] = []
    if not records:
        return labels
    centers = {(round(r.center[0], 2), round(r.center[1], 2)) for r in records}
    radii = [r.diameter for r in records]
    if len(centers) == 1:
        labels.append("SINGLE_POINT_CHILD_ACCUMULATION")
    elif len(centers) <= 4:
        labels.append("FINITE_CENTER_CHILD_ACCUMULATION")
    else:
        labels.append("DIFFUSE_CHILD_CENTER_DISTRIBUTION")
    if records[-1].param_interval[1] >= 0.95:
        labels.append("PARAMETER_ENDPOINT_ACCUMULATION")
    if radii and min(radii) > 0.12:
        labels.append("POSITIVE_SCALE_CHILDREN")
    return labels


def build_countably_branching_tree(
    *,
    child_count: int = 24,
    lambda_ratio: float = 0.72,
    depth_after: int = 1,
) -> CanonicalIntrusionTree:
    """Root with many children (countable proxy) + optional finite tail depth."""
    nodes: dict[str, IntrusionTreeNode] = {}
    root_id = "root"
    nodes[root_id] = IntrusionTreeNode(
        node_id=root_id,
        param_interval=(0.0, 1.0),
        diameter=1.0,
        defect=0.1,
        gate_count=4,
        center=(0.5, 0.5),
        sign=1,
        parent_id=None,
        child_ids=[],
        jordan_hull=True,
        gate_class="FINITE_MULTIGATE",
    )
    r = 0.5
    for i in range(child_count):
        cid = f"c{i}"
        p0 = i / max(child_count, 1)
        p1 = (i + 1) / max(child_count, 1)
        nodes[cid] = IntrusionTreeNode(
            node_id=cid,
            param_interval=(p0, p1),
            diameter=r,
            defect=0.02 * r * r,
            gate_count=2,
            center=(0.5 + 0.001 * i, 0.5),
            sign=1,
            parent_id=root_id,
            child_ids=[],
            jordan_hull=True,
            gate_class="TWO_GATE",
        )
        nodes[root_id].child_ids.append(cid)
        r *= lambda_ratio
        if depth_after > 0 and i < 4:
            leaf = f"c{i}_L"
            nodes[leaf] = IntrusionTreeNode(
                node_id=leaf,
                param_interval=(p0, p1),
                diameter=r * 0.8,
                defect=0.01 * r * r,
                gate_count=2,
                center=(0.5, 0.5),
                sign=1,
                parent_id=cid,
                child_ids=[],
                jordan_hull=True,
                gate_class="TWO_GATE",
            )
            nodes[cid].child_ids.append(leaf)
    tree_class: TreeClass = (
        "INFINITE_LOCAL_BRANCHING_TREE" if child_count >= 20 else "LOCALLY_FINITE_INTRUSION_TREE"
    )
    depth = 2 if depth_after else 1
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class=tree_class,
        order_independent=True,
        depth=depth,
    )


def extract_countable_family(tree: CanonicalIntrusionTree, parent_id: str) -> CountableChildFamily | None:
    if parent_id not in tree.nodes:
        return None
    parent = tree.nodes[parent_id]
    children = [tree.nodes[c] for c in parent.child_ids if c in tree.nodes]
    records = canonical_child_order(parent, children)
    labels = classify_child_accumulation(records)
    return CountableChildFamily(
        parent_id=parent_id,
        children=records,
        canonical_order=True,
        accumulation_labels=labels,
    )
