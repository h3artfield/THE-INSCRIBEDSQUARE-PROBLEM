"""Tree end cylinders [v] (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_tree_boundary import TreeEndClass, build_tree_boundary


@dataclass
class EndCylinder:
    node_id: str
    end_ids: list[str]
    mass_fraction: float
    diameter: float
    depth: int


@dataclass
class CylinderPartitionAudit:
    cylinders: list[EndCylinder]
    partition_valid: bool
    nested_prefix: bool
    child_partition: bool
    messages: list[str]


def _depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def _ends_under(tree: CanonicalIntrusionTree, nid: str, ends: list[TreeEndClass]) -> list[str]:
    desc: set[str] = set()

    def collect(n: str) -> None:
        desc.add(n)
        for c in tree.nodes[n].child_ids:
            if c in tree.nodes:
                collect(c)

    collect(nid)
    return [e.end_id for e in ends if e.end_id in desc]


def build_cylinder(tree: CanonicalIntrusionTree, node_id: str) -> EndCylinder:
    ends = build_tree_boundary(tree)
    end_ids = _ends_under(tree, node_id, ends)
    node = tree.nodes[node_id]
    total = len(ends) or 1
    return EndCylinder(
        node_id=node_id,
        end_ids=end_ids,
        mass_fraction=len(end_ids) / total,
        diameter=node.diameter,
        depth=_depth(tree, node_id),
    )


def audit_cylinder_partition(tree: CanonicalIntrusionTree, parent_id: str) -> CylinderPartitionAudit:
    """Child cylinders partition [parent]."""
    parent = tree.nodes.get(parent_id)
    if not parent:
        return CylinderPartitionAudit([], False, True, False, ["missing parent"])
    ends = build_tree_boundary(tree)
    child_cylinders = [build_cylinder(tree, cid) for cid in parent.child_ids if cid in tree.nodes]
    child_end_sets = [set(c.end_ids) for c in child_cylinders]
    parent_ends = set(_ends_under(tree, parent_id, ends))
    union = set().union(*child_end_sets) if child_end_sets else set()
    partition = union == parent_ends and all(
        len(child_end_sets[i] & child_end_sets[j]) == 0
        for i in range(len(child_end_sets))
        for j in range(i + 1, len(child_end_sets))
    )
    nested = all(
        c.depth >= _depth(tree, parent_id) for c in child_cylinders
    )
    return CylinderPartitionAudit(
        cylinders=child_cylinders,
        partition_valid=partition or not parent.child_ids,
        nested_prefix=nested,
        child_partition=partition or len(parent.child_ids) <= 1,
        messages=[f"partition={partition}, children={len(child_cylinders)}"],
    )


def build_antichain(tree: CanonicalIntrusionTree, *, max_depth: int = 3) -> list[str]:
    """Finite antichain of maximal unresolved nodes at depth <= max_depth."""
    ids: list[str] = []
    for nid, node in tree.nodes.items():
        if _depth(tree, nid) > max_depth:
            continue
        if node.child_ids and all(_depth(tree, c) <= max_depth for c in node.child_ids if c in tree.nodes):
            ids.append(nid)
        elif not node.child_ids:
            ids.append(nid)
    return ids or [tree.root_id]
