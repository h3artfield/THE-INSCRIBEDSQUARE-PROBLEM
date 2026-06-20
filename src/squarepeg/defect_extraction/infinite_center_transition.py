"""Infinite-center transition geometry (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure

CenterClass = Literal[
    "UNIFORMLY_FINITE",
    "SLOWLY_DIVERGING",
    "DIFFUSE_CENTERS",
    "BOUNDARY_SUPPORTED",
    "PARAMETER_DISCONNECTED",
]


@dataclass
class InfiniteCenterRecord:
    parent_id: str
    center_cover_number: int
    center_class: CenterClass
    packing_route: str


@dataclass
class InfiniteCenterTransitionAudit:
    records: list[InfiniteCenterRecord]
    infinite_center_remains: bool
    messages: list[str]


def _cover_number(tree, parent_id: str) -> int:
    node = tree.nodes[parent_id]
    centers = set()
    for cid in node.child_ids:
        if cid in tree.nodes:
            c = tree.nodes[cid]
            key = (round(c.center[0], 2), round(c.center[1], 2))
            centers.add(key)
    return max(len(centers), 1)


def audit_infinite_center_transition(tree: CanonicalIntrusionTree) -> InfiniteCenterTransitionAudit:
    child = audit_child_transition_measure(tree)
    states = audit_augmented_neutral_state(tree)
    state_map = {s.node_id: s for s in states.states}
    records: list[InfiniteCenterRecord] = []
    infinite = False
    for m in child.measures:
        nc = _cover_number(tree, m.parent_id)
        cc: CenterClass = "UNIFORMLY_FINITE"
        route = "T062_FINITE_CENTER"
        if nc > 6:
            cc = "DIFFUSE_CENTERS"
            route = "INFINITE_CENTER_TRANSITION"
            infinite = True
        elif nc > 3:
            cc = "SLOWLY_DIVERGING"
            route = "T087_PACKING"
        records.append(InfiniteCenterRecord(m.parent_id, nc, cc, route))
    return InfiniteCenterTransitionAudit(
        records=records,
        infinite_center_remains=infinite,
        messages=[f"records={len(records)}, infinite={infinite}"],
    )
