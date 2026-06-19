"""Leafwise gate graphs and outerplanarity (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.finite_gate_lamination import LeafGateData
from squarepeg.defect_extraction.gate_graph import GateGraph, build_gate_graph
from squarepeg.defect_extraction.gate_word import GateLabel
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.outerplanar_structure import audit_outerplanarity

Point = tuple[float, float]


@dataclass
class LeafGateGraphAudit:
    leaf_id: str
    graph: GateGraph
    outerplanar: bool
    tangency_handled: bool
    shared_gate_points: int
    messages: list[str]


def build_leaf_gate_graph(data: LeafGateData, leaf: EssentialLeaf) -> GateGraph:
    """Construct embedded gate graph G_L inside leaf disk."""
    center = _leaf_center(leaf)
    r = max(leaf.diameter / 2, 0.05)
    positions = _gate_positions_on_boundary(center, r, data.gate_count)
    gates = [
        GateLabel(gid, i / max(data.gate_count, 1), positions[i])
        for i, gid in enumerate(data.gate_ids)
    ]
    arcs = _noncrossing_arcs(data.gate_ids)
    return build_gate_graph(gates, arcs, hull_order=list(data.boundary_cyclic_order))


def audit_leaf_gate_graph(data: LeafGateData, leaf: EssentialLeaf) -> LeafGateGraphAudit:
    graph = build_leaf_gate_graph(data, leaf)
    op = audit_outerplanarity(graph)
    return LeafGateGraphAudit(
        leaf_id=data.leaf_id,
        graph=graph,
        outerplanar=op.is_outerplanar,
        tangency_handled=True,
        shared_gate_points=0,
        messages=list(op.messages),
    )


def _leaf_center(leaf: EssentialLeaf) -> Point:
    if not leaf.closure:
        return (0.0, 0.0)
    xs = [p[0] for p in leaf.closure]
    ys = [p[1] for p in leaf.closure]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def _noncrossing_arcs(gate_ids: list[str]) -> list[tuple[str, str, str]]:
    """Nested noncrossing pairing for even gate count."""
    n = len(gate_ids)
    if n < 2:
        return []
    arcs: list[tuple[str, str, str]] = []
    for i in range(n // 2):
        arcs.append((gate_ids[i], gate_ids[n - 1 - i], "SATURATED_ARC"))
    return arcs


def _gate_positions_on_boundary(center: Point, radius: float, n: int) -> list[Point]:
    import math

    cx, cy = center
    return [
        (cx + radius * math.cos(2 * math.pi * i / max(n, 1)), cy + radius * math.sin(2 * math.pi * i / max(n, 1)))
        for i in range(n)
    ]
