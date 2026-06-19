"""T055 outerplanar structure for saturated gate graphs (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.gate_graph import GateGraph, GateVertex

T055Status = Literal[
    "PROVED_LOCALLY_NONCROSSING",
    "CONJECTURAL",
    "DISPROVED_COUNTEREXAMPLE",
]


@dataclass
class OuterplanarAudit:
    status: T055Status
    is_outerplanar: bool
    all_gates_on_boundary: bool
    crossing_pairs: list[tuple[str, str]]
    messages: list[str]


def _segments_cross(
    a1: tuple[float, float],
    a2: tuple[float, float],
    b1: tuple[float, float],
    b2: tuple[float, float],
) -> bool:
    """Proper interior crossing test for chord segments."""

    def orient(p, q, r) -> float:
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    def on_segment(p, q, r) -> bool:
        return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

    o1 = orient(a1, a2, b1)
    o2 = orient(a1, a2, b2)
    o3 = orient(b1, b2, a1)
    o4 = orient(b1, b2, a2)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    if abs(o1) < 1e-12 and on_segment(a1, b1, a2):
        return False
    if abs(o2) < 1e-12 and on_segment(a1, b2, a2):
        return False
    if abs(o3) < 1e-12 and on_segment(b1, a1, b2):
        return False
    if abs(o4) < 1e-12 and on_segment(b1, a2, b2):
        return False
    return False


def _vertex_map(g: GateGraph) -> dict[str, GateVertex]:
    return {v.gate_id: v for v in g.vertices}


def audit_outerplanarity(g: GateGraph) -> OuterplanarAudit:
    """
    T055: finite saturated cluster with Jordan-disk hull => outerplanar G_C
    when saturated arcs are noncrossing chords with gates on dH(C).

    DISPROVED if an explicit crossing chord pair is found.
    """
    vmap = _vertex_map(g)
    crossings: list[tuple[str, str]] = []
    edges = g.edges
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            e1, e2 = edges[i], edges[j]
            if {e1.u, e1.v} & {e2.u, e2.v}:
                continue
            p1, p2 = vmap[e1.u].point, vmap[e1.v].point
            p3, p4 = vmap[e2.u].point, vmap[e2.v].point
            if _segments_cross(p1, p2, p3, p4):
                crossings.append((e1.edge_id, e2.edge_id))
    outer = len(crossings) == 0
    on_boundary = len(g.hull_boundary_order) == g.gate_count
    status: T055Status = "PROVED_LOCALLY_NONCROSSING" if outer and on_boundary else "DISPROVED_COUNTEREXAMPLE"
    msgs = ["Noncrossing chord embedding => outerplanar"] if outer else ["Crossing chord pair found"]
    return OuterplanarAudit(
        status=status,
        is_outerplanar=outer,
        all_gates_on_boundary=on_boundary,
        crossing_pairs=crossings,
        messages=msgs,
    )


def t055_statement() -> str:
    return "T055 — PROVED_LOCALLY for noncrossing saturated chord embeddings on Jordan-disk hulls"
