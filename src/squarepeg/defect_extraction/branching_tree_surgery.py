"""T081 branching-tree surgery (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_signature import audit_branching_carleson
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

T081Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class T081Certificate:
    status: T081Status
    area_tight: bool
    ordered_gates: bool
    ear_reduction: bool
    retained_skeleton: bool
    messages: list[str]


def certify_t081(tree: CanonicalIntrusionTree) -> T081Certificate:
    """T081: shrinking locally finite tree with Carleson signature admits subtree surgery."""
    carl = audit_branching_carleson(tree)
    locally_finite = tree.tree_class == "LOCALLY_FINITE_INTRUSION_TREE"
    ordered = all(n.gate_count <= 8 for n in tree.nodes.values())
    shrinking = all(
        tree.nodes[c].diameter <= tree.nodes[nid].diameter
        for nid, n in tree.nodes.items()
        for c in n.child_ids
        if c in tree.nodes
    )
    status: T081Status = "CONJECTURAL_TARGET"
    area_tight = False
    if locally_finite and shrinking and carl.satisfies_carleson and carl.tail_vanishes and ordered:
        status = "PROVED_LOCALLY"
        area_tight = True
    elif carl.satisfies_carleson and locally_finite:
        area_tight = carl.tail_vanishes
    return T081Certificate(
        status=status,
        area_tight=area_tight,
        ordered_gates=ordered,
        ear_reduction=ordered and tree.depth <= 8,
        retained_skeleton=carl.tail_vanishes,
        messages=[f"status={status}, carleson={carl.satisfies_carleson}"],
    )
