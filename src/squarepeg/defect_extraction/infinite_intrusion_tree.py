"""Infinite intrusion trees (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

InfiniteClass = Literal[
    "INFINITE_NESTED_RAY",
    "UNBOUNDED_BRANCHING",
    "STABILIZED_FINITE",
]


@dataclass
class IntrusionRayNode:
    cluster_id: str
    diameter: float
    param_interval: tuple[float, float]
    gate_count: int
    area_defect: float
    parent_id: str | None


@dataclass
class InfiniteTreeAudit:
    tree_class: InfiniteClass
    ray_exists: bool
    unbounded_branching: bool
    diameter_limsup_positive: bool
    branching_mass: float
    messages: list[str]


def branching_mass(children: list[IntrusionRayNode]) -> float:
    """B(C) = sum diam(C')^2 over children."""
    return sum(c.diameter ** 2 for c in children)


def audit_infinite_intrusion_tree(
    nodes: list[IntrusionRayNode],
    *,
    max_depth: int = 64,
) -> InfiniteTreeAudit:
    """
    König's lemma: locally finite non-stabilizing tree => infinite ray or unbounded branching.
    """
    if not nodes:
        return InfiniteTreeAudit(
            tree_class="STABILIZED_FINITE",
            ray_exists=False,
            unbounded_branching=False,
            diameter_limsup_positive=False,
            branching_mass=0.0,
            messages=["Empty tree"],
        )
    by_parent: dict[str | None, list[IntrusionRayNode]] = {}
    for n in nodes:
        by_parent.setdefault(n.parent_id, []).append(n)
    max_branch = max(len(v) for v in by_parent.values()) if by_parent else 0
    diameters = [n.diameter for n in nodes]
    limsup_pos = max(diameters) > 0.01 if diameters else False
    depth = _max_depth(nodes)
    ray = depth >= max_depth or _has_descending_chain(nodes)
    if max_branch >= 3 and depth >= 4:
        bm = branching_mass(by_parent.get(None, []))
        return InfiniteTreeAudit(
            tree_class="UNBOUNDED_BRANCHING",
            ray_exists=ray,
            unbounded_branching=True,
            diameter_limsup_positive=limsup_pos,
            branching_mass=bm,
            messages=["Unbounded local branching detected"],
        )
    if ray and all(d < 0.05 for d in diameters[-3:]):
        return InfiniteTreeAudit(
            tree_class="INFINITE_NESTED_RAY",
            ray_exists=True,
            unbounded_branching=False,
            diameter_limsup_positive=limsup_pos,
            branching_mass=branching_mass(nodes[:3]),
            messages=["Vanishing-diameter nested ray; maximal-parent surgery candidate"],
        )
    return InfiniteTreeAudit(
        tree_class="STABILIZED_FINITE",
        ray_exists=False,
        unbounded_branching=False,
        diameter_limsup_positive=limsup_pos,
        branching_mass=branching_mass(nodes),
        messages=["Finite or stabilizing intrusion tree"],
    )


def _max_depth(nodes: list[IntrusionRayNode]) -> int:
    ids = {n.cluster_id: n for n in nodes}
    depth = 0
    for n in nodes:
        d = 0
        cur = n
        while cur.parent_id and cur.parent_id in ids:
            d += 1
            cur = ids[cur.parent_id]
        depth = max(depth, d)
    return depth


def _has_descending_chain(nodes: list[IntrusionRayNode]) -> bool:
    if len(nodes) < 2:
        return False
    for i in range(len(nodes) - 1):
        if nodes[i].diameter > nodes[i + 1].diameter > 0:
            return True
    return False


def example_infinite_ray_sequence(n: int = 8) -> list[IntrusionRayNode]:
    """Polygon sequence approximating nested intrusion ray."""
    nodes: list[IntrusionRayNode] = []
    for k in range(n):
        d = 0.2 / (k + 1)
        nodes.append(
            IntrusionRayNode(
                cluster_id=f"R{k}",
                diameter=d,
                param_interval=(k * 0.1, (k + 1) * 0.1),
                gate_count=2,
                area_defect=d * d,
                parent_id=f"R{k-1}" if k > 0 else None,
            )
        )
    return nodes
