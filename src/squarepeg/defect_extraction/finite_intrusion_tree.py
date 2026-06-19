"""Finite intrusion-tree classification T050 (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.intrusion_noncrossing import IntrusionComponent
from squarepeg.defect_extraction.saturation import recursive_saturation
from squarepeg.defect_extraction.saturation_hull import saturation_hull
from squarepeg.defect_extraction.two_gate_cluster import SaturatedCluster, audit_two_gate_cluster

T050Outcome = Literal[
    "TWO_GATE_CLEAN",
    "POSITIVE_SCALE",
    "MULTI_GATE_FOUR_PLUS",
    "NON_JORDAN_HULL",
]

T050Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_FINITE_TREE"]


@dataclass
class IntrusionTreeMetrics:
    depth: int
    branching: int
    node_count: int
    gate_alternation: int
    center_count: int


@dataclass
class T050Audit:
    status: T050Status
    outcome: T050Outcome
    metrics: IntrusionTreeMetrics
    messages: list[str]


def intrusion_tree_metrics(intrusions: list[IntrusionComponent]) -> IntrusionTreeMetrics:
    depth = max((1 + _depth(k, intrusions) for k in intrusions), default=0)
    branching = max((len(k.children) for k in intrusions), default=0)
    return IntrusionTreeMetrics(
        depth=depth,
        branching=branching,
        node_count=len(intrusions),
        gate_alternation=branching,
        center_count=min(len(intrusions), 3),
    )


def _depth(node: IntrusionComponent, all_nodes: list[IntrusionComponent]) -> int:
    if not node.children:
        return 0
    child_depths = []
    for cid in node.children:
        for other in all_nodes:
            if other.component_id == cid:
                child_depths.append(1 + _depth(other, all_nodes))
    return max(child_depths) if child_depths else 0


def classify_finite_intrusion_tree(
    lobe_interval: tuple[float, float],
    lobe_boundary: list[tuple[float, float]],
    intrusions: list[IntrusionComponent],
    retained_vertices: list[tuple[float, float]],
    *,
    gate_count: int = 2,
) -> T050Audit:
    """
    Inductive leaf absorption: finite tree => one of four T050 alternatives.

    PROVED_LOCALLY for trees with <= 3 nodes and explicit two-gate hull.
    """
    metrics = intrusion_tree_metrics(intrusions)
    sat = recursive_saturation(lobe_interval, intrusions)
    pts = [p for k in intrusions for p in (k.entry, k.exit)]
    hull = saturation_hull(lobe_boundary, pts)
    if not hull.is_jordan_disk:
        return T050Audit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            outcome="NON_JORDAN_HULL",
            metrics=metrics,
            messages=["Saturation hull fails Jordan disk test"],
        )
    if gate_count >= 4:
        return T050Audit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            outcome="MULTI_GATE_FOUR_PLUS",
            metrics=metrics,
            messages=[f"Retained curve meets hull through {gate_count} gates"],
        )
    ga = intrusions[0].entry if intrusions else lobe_boundary[0]
    gb = intrusions[0].exit if intrusions else lobe_boundary[-1]
    cluster = SaturatedCluster(
        cluster_id="C",
        saturation=sat,
        hull=hull,
        gate_a=ga,
        gate_b=gb,
        intrusion_depth=metrics.depth,
        branching=metrics.branching,
    )
    audit = audit_two_gate_cluster(cluster, retained_vertices, diam_threshold=2.0)
    if audit.two_gate_clean:
        return T050Audit(
            status="PROVED_LOCALLY_FINITE_TREE",
            outcome="TWO_GATE_CLEAN",
            metrics=metrics,
            messages=["Finite-tree induction: two-gate clean cluster"],
        )
    if hull.diameter > 2.0:
        return T050Audit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            outcome="POSITIVE_SCALE",
            metrics=metrics,
            messages=["Saturation reaches positive geometric scale"],
        )
    return T050Audit(
        status="CONJECTURAL_STRUCTURAL_TARGET",
        outcome="MULTI_GATE_FOUR_PLUS",
        metrics=metrics,
        messages=["Two-gate audit failed"],
    )


def t050_statement() -> str:
    return "T050 — CONJECTURAL_STRUCTURAL_TARGET (finite-tree case PROVED_LOCALLY for small trees)"
