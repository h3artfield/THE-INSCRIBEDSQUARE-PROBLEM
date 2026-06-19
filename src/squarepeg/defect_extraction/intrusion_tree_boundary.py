"""Intrusion tree boundary and end space (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

BoundaryTopology = Literal[
    "LOCALLY_FINITE_CYLINDER",
    "COUNTABLY_BRANCHING_CYLINDER",
]


@dataclass
class TreeRay:
    node_ids: list[str]
    param_intervals: list[tuple[float, float]]


@dataclass
class TreeEndClass:
    end_id: str
    ray_prefix: tuple[str, ...]
    terminal_leaf: str | None
    spatial_center: tuple[float, float] | None


@dataclass
class TreeBoundaryAudit:
    topology: BoundaryTopology
    ends: list[TreeEndClass]
    compact: bool
    countably_branching: bool
    cylinder_measurable: bool
    messages: list[str]


def _extract_rays(tree: CanonicalIntrusionTree) -> list[TreeRay]:
    rays: list[TreeRay] = []

    def walk(nid: str, path: list[str], intervals: list[tuple[float, float]]) -> None:
        node = tree.nodes[nid]
        path = path + [nid]
        intervals = intervals + [node.param_interval]
        if not node.child_ids:
            rays.append(TreeRay(path, intervals))
            return
        for cid in node.child_ids:
            if cid in tree.nodes:
                walk(cid, path, intervals)

    if tree.root_id in tree.nodes:
        walk(tree.root_id, [], [])
    return rays


def _ray_prefix_key(ray: TreeRay, length: int) -> tuple[str, ...]:
    return tuple(ray.node_ids[:length])


def build_tree_boundary(tree: CanonicalIntrusionTree) -> list[TreeEndClass]:
    """Ends as equivalence classes of infinite rays sharing finite prefixes (leaf proxy)."""
    rays = _extract_rays(tree)
    ends: list[TreeEndClass] = []
    seen: set[str] = set()
    for ray in rays:
        terminal = ray.node_ids[-1]
        if terminal in seen:
            continue
        seen.add(terminal)
        node = tree.nodes[terminal]
        ends.append(
            TreeEndClass(
                end_id=terminal,
                ray_prefix=_ray_prefix_key(ray, len(ray.node_ids)),
                terminal_leaf=terminal,
                spatial_center=node.center,
            )
        )
    return ends


def audit_tree_boundary(tree: CanonicalIntrusionTree) -> TreeBoundaryAudit:
    ends = build_tree_boundary(tree)
    countably = tree.tree_class == "INFINITE_LOCAL_BRANCHING_TREE"
    topology: BoundaryTopology = (
        "COUNTABLY_BRANCHING_CYLINDER" if countably else "LOCALLY_FINITE_CYLINDER"
    )
    compact = not countably or all(
        tree.nodes[e.end_id].diameter < 0.5 for e in ends if e.end_id in tree.nodes
    )
    return TreeBoundaryAudit(
        topology=topology,
        ends=ends,
        compact=compact,
        countably_branching=countably,
        cylinder_measurable=True,
        messages=[f"topology={topology}, ends={len(ends)}, compact={compact}"],
    )
