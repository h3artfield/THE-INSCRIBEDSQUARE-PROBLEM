"""Intrusion gate graph G_C (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.gate_word import GateLabel

Point = tuple[float, float]

EdgeKind = Literal[
    "SATURATED_ARC",
    "RETAINED_ARC",
    "HULL_BOUNDARY",
    "DEGENERATE",
]


@dataclass
class GateVertex:
    gate_id: str
    point: Point
    param_index: float
    hull_index: int


@dataclass
class GateEdge:
    edge_id: str
    u: str
    v: str
    kind: EdgeKind
    interior_points: list[Point] = field(default_factory=list)
    multiplicity: int = 1


@dataclass
class GateGraph:
    """Embedded intrusion gate graph G_C inside H(C)."""

    vertices: list[GateVertex]
    edges: list[GateEdge]
    hull_boundary_order: list[str]

    @property
    def gate_count(self) -> int:
        return len(self.vertices)

    @property
    def vertex_ids(self) -> list[str]:
        return [v.gate_id for v in self.vertices]


def build_gate_graph(
    gates: list[GateLabel],
    arcs: list[tuple[str, str, EdgeKind]],
    *,
    hull_order: list[str] | None = None,
) -> GateGraph:
    """Build G_C from gate labels and internal saturated arcs."""
    verts = [
        GateVertex(g.gate_id, g.point, g.param_index, i)
        for i, g in enumerate(gates)
    ]
    h_order = hull_order or [g.gate_id for g in sorted(gates, key=lambda x: x.param_index)]
    edges: list[GateEdge] = []
    for k, (u, v, kind) in enumerate(arcs):
        edges.append(GateEdge(edge_id=f"e{k}", u=u, v=v, kind=kind))
    return GateGraph(vertices=verts, edges=edges, hull_boundary_order=h_order)


def example_four_gate_graph() -> GateGraph:
    """Noncrossing 4-gate matching: (g0,g3), (g1,g2)."""
    gates = [
        GateLabel("g0", 0.0, (0.0, 1.0)),
        GateLabel("g1", 0.25, (1.0, 0.0)),
        GateLabel("g2", 0.5, (0.0, -1.0)),
        GateLabel("g3", 0.75, (-1.0, 0.0)),
    ]
    arcs = [
        ("g0", "g3", "SATURATED_ARC"),
        ("g1", "g2", "SATURATED_ARC"),
    ]
    return build_gate_graph(gates, arcs, hull_order=["g0", "g1", "g2", "g3"])


def example_nested_six_gate_graph() -> GateGraph:
    """Nested noncrossing matching on 6 boundary gates."""
    gates = [GateLabel(f"g{i}", i / 6.0, (float(i), 0.0)) for i in range(6)]
    arcs = [("g0", "g5", "SATURATED_ARC"), ("g1", "g4", "SATURATED_ARC"), ("g2", "g3", "SATURATED_ARC")]
    return build_gate_graph(gates, arcs)
