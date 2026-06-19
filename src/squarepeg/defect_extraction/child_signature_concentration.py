"""Child signature concentration–compactness (Directive 043)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode
from squarepeg.defect_extraction.child_center_measure import (
    ChildCenterMeasure,
    build_child_center_measure,
)
from squarepeg.defect_extraction.countable_child_order import CountableChildFamily, extract_countable_family

ConcentrationBranch = Literal[
    "CONCENTRATED",
    "FINITE_CENTER",
    "DIFFUSE",
    "HULL_DEGENERATION",
]

ConcentratedOutcome = Literal[
    "PARAMETER_CONSECUTIVE_CLUSTER",
    "FINITE_PARAMETER_BLOCKS",
    "DISCONNECTED_CONCENTRATION",
    "SMALLER_NONSUMMABLE_RAY",
    "NONE",
]


@dataclass
class ChildConcentrationRecord:
    parent_id: str
    branch: ConcentrationBranch
    mass_in_shrinking_ball: float
    center_count: int
    hull_jordan: bool
    concentrated_outcome: ConcentratedOutcome


@dataclass
class ChildConcentrationAudit:
    records: list[ChildConcentrationRecord]
    primary_branch: ConcentrationBranch
    routes_t064: bool
    routes_t062: bool
    diffuse_child_center: bool
    hull_degenerate: bool
    messages: list[str]


def _ball_mass(measure: ChildCenterMeasure, *, radius: float = 0.15) -> float:
    if not measure.atoms:
        return 0.0
    cx = sum(a.center[0] * a.weight for a in measure.atoms)
    cy = sum(a.center[1] * a.weight for a in measure.atoms)
    return sum(
        a.weight
        for a in measure.atoms
        if (a.center[0] - cx) ** 2 + (a.center[1] - cy) ** 2 <= radius * radius
    )


def _classify_branch(measure: ChildCenterMeasure, *, K: int = 4) -> ConcentrationBranch:
    ball_mass = _ball_mass(measure)
    centers = len({(round(a.center[0], 1), round(a.center[1], 1)) for a in measure.atoms})
    if ball_mass >= 0.55:
        return "CONCENTRATED"
    if centers <= K:
        return "FINITE_CENTER"
    return "DIFFUSE"


def _concentrated_outcome(family: CountableChildFamily, measure: ChildCenterMeasure) -> ConcentratedOutcome:
    if _ball_mass(measure) < 0.55:
        return "NONE"
    intervals = [r.param_interval for r in family.children]
    consecutive = all(
        abs(intervals[i][1] - intervals[i + 1][0]) < 0.05 for i in range(len(intervals) - 1)
    )
    if consecutive:
        return "PARAMETER_CONSECUTIVE_CLUSTER"
    blocks = len({round(r.param_interval[0], 1) for r in family.children})
    if blocks <= 3:
        return "FINITE_PARAMETER_BLOCKS"
    centers = len({(round(a.center[0], 1), round(a.center[1], 1)) for a in measure.atoms})
    if centers > 2:
        return "DISCONNECTED_CONCENTRATION"
    return "SMALLER_NONSUMMABLE_RAY"


def audit_child_signature_concentration(
    tree: CanonicalIntrusionTree,
    *,
    K: int = 4,
) -> ChildConcentrationAudit:
    records: list[ChildConcentrationRecord] = []
    for nid, node in tree.nodes.items():
        if len(node.child_ids) < 3:
            continue
        fam = extract_countable_family(tree, nid)
        if not fam:
            continue
        measure = build_child_center_measure(fam)
        branch = _classify_branch(measure, K=K)
        ball = _ball_mass(measure)
        centers = len({(round(a.center[0], 1), round(a.center[1], 1)) for a in measure.atoms})
        hull_ok = all(tree.nodes[c].jordan_hull for c in node.child_ids if c in tree.nodes)
        outcome = _concentrated_outcome(fam, measure) if branch == "CONCENTRATED" else "NONE"
        records.append(
            ChildConcentrationRecord(nid, branch, ball, centers, hull_ok, outcome)
        )

    primary: ConcentrationBranch = "DIFFUSE"
    if records:
        by_mass = max(records, key=lambda r: r.mass_in_shrinking_ball)
        primary = by_mass.branch

    hull_deg = any(not r.hull_jordan for r in records)
    if hull_deg:
        primary = "HULL_DEGENERATION"

    return ChildConcentrationAudit(
        records=records,
        primary_branch=primary,
        routes_t064=bool(records) and primary == "CONCENTRATED",
        routes_t062=bool(records) and primary == "FINITE_CENTER",
        diffuse_child_center=bool(records) and primary == "DIFFUSE",
        hull_degenerate=hull_deg,
        messages=[f"primary={primary}, records={len(records)}"],
    )


def build_concentrated_child_tree(*, child_count: int = 12) -> CanonicalIntrusionTree:
    """Children with mass concentrating in shrinking balls."""
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
    )
    r = 0.4
    for i in range(child_count):
        cid = f"c{i}"
        p0, p1 = i / child_count, (i + 1) / child_count
        nodes[cid] = IntrusionTreeNode(
            node_id=cid,
            param_interval=(p0, p1),
            diameter=r,
            defect=0.03 * r,
            gate_count=2,
            center=(0.5 + 0.002 * i, 0.5 + 0.001 * i),
            sign=1,
            parent_id=root_id,
            child_ids=[],
            jordan_hull=True,
        )
        nodes[root_id].child_ids.append(cid)
        r *= 0.75
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class="INFINITE_LOCAL_BRANCHING_TREE" if child_count >= 20 else "LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=1,
    )


def build_uniform_circle_child_centers(*, child_count: int = 16) -> CanonicalIntrusionTree:
    """Children uniformly distributed on a circle (finite-center proxy)."""
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
    )
    r = 0.35
    for i in range(child_count):
        angle = 2 * math.pi * i / child_count
        cid = f"c{i}"
        p0, p1 = i / child_count, (i + 1) / child_count
        nodes[cid] = IntrusionTreeNode(
            node_id=cid,
            param_interval=(p0, p1),
            diameter=r,
            defect=0.025 * r,
            gate_count=2,
            center=(0.5 + 0.2 * math.cos(angle), 0.5 + 0.2 * math.sin(angle)),
            sign=(-1) ** i,
            parent_id=root_id,
            child_ids=[],
            jordan_hull=True,
        )
        nodes[root_id].child_ids.append(cid)
        r *= 0.82
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class="INFINITE_LOCAL_BRANCHING_TREE",
        order_independent=True,
        depth=1,
    )


def build_cantor_child_center_tree(*, child_count: int = 24) -> CanonicalIntrusionTree:
    """Cantor-distributed child centers."""
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
    )
    r = 0.3
    for i in range(child_count):
        t = i / child_count
        cx = 0.5 + 0.35 * (2 * (t * 7 % 1) - 1) * (0.5 + 0.5 * math.sin(i))
        cy = 0.5 + 0.35 * (2 * (t * 11 % 1) - 1) * (0.5 + 0.5 * math.cos(i))
        cid = f"c{i}"
        p0, p1 = t, (i + 1) / child_count
        nodes[cid] = IntrusionTreeNode(
            node_id=cid,
            param_interval=(p0, p1),
            diameter=r,
            defect=0.02 * r * r,
            gate_count=2 + (i % 3),
            center=(cx, cy),
            sign=1 if i % 2 == 0 else -1,
            parent_id=root_id,
            child_ids=[],
            jordan_hull=True,
        )
        nodes[root_id].child_ids.append(cid)
        r *= 0.78
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class="INFINITE_LOCAL_BRANCHING_TREE",
        order_independent=True,
        depth=1,
    )
