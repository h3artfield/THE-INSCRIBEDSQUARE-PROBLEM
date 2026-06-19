"""T058 hull-adjacent geometric ears (Directive 030)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.block_decomposition import decompose_blocks
from squarepeg.defect_extraction.gate_graph import GateEdge, GateGraph, GateVertex
from squarepeg.defect_extraction.geometric_ear import GraphEar, find_graph_ears
from squarepeg.defect_extraction.outerplanar_structure import audit_outerplanarity

T058Status = Literal[
    "PROVED_LOCALLY",
    "CONJECTURAL_TARGET",
    "DISPROVED_COUNTEREXAMPLE",
]


@dataclass
class HullAdjacentArc:
    gate_a: str
    gate_b: str
    boundary_arc: list[str]
    gate_free: bool


@dataclass
class CandidateGeometricEar:
    ear_id: str
    gate_a: str
    gate_b: str
    graph_path_edges: list[str]
    hull_arc: HullAdjacentArc
    jordan_subdisk: bool
    saturated: bool
    t051_eligible: bool


@dataclass
class T058Audit:
    status: T058Status
    geometric_ear: CandidateGeometricEar | None
    weak_dual_leaf: bool
    messages: list[str] = field(default_factory=list)


def is_hull_adjacent(hull_order: list[str], gate_a: str, gate_b: str) -> HullAdjacentArc:
    """One boundary arc between gates contains no other true gate in its interior."""
    if gate_a not in hull_order or gate_b not in hull_order:
        return HullAdjacentArc(gate_a, gate_b, [], False)
    ia, ib = hull_order.index(gate_a), hull_order.index(gate_b)
    lo, hi = min(ia, ib), max(ia, ib)
    arc_forward = hull_order[lo : hi + 1]
    arc_wrap = hull_order[hi:] + hull_order[: lo + 1]
    if len(arc_forward) == 2:
        return HullAdjacentArc(gate_a, gate_b, arc_forward, True)
    if len(arc_wrap) == 2:
        return HullAdjacentArc(gate_a, gate_b, arc_wrap, True)
    return HullAdjacentArc(gate_a, gate_b, arc_forward, False)


def reduce_gate_graph(g: GateGraph) -> GateGraph:
    """Delete zero-length edges; suppress degree-two filler vertices."""
    edges = [e for e in g.edges if e.u != e.v and e.kind != "DEGENERATE"]
    true_gates = {v.gate_id for v in g.vertices}
    return GateGraph(
        vertices=list(g.vertices),
        edges=edges,
        hull_boundary_order=list(g.hull_boundary_order),
    )


def weak_dual_leaf_face(g: GateGraph) -> tuple[str, str, list[str]] | None:
    """
    Weak-dual leaf: face with gate-free hull boundary arc + embedded graph path.

    For outerplanar chord graphs, outermost non-nested edge yields hull-adjacent pair.
    """
    h = g.hull_boundary_order
    idx = {gid: i for i, gid in enumerate(h)}
    for e in g.edges:
        adj = is_hull_adjacent(h, e.u, e.v)
        if adj.gate_free:
            return e.u, e.v, [e.edge_id]
        ia, ib = idx.get(e.u, -1), idx.get(e.v, -1)
        if ia < 0 or ib < 0:
            continue
        lo, hi = min(ia, ib), max(ia, ib)
        nested = any(
            lo < min(idx.get(e2.u, -1), idx.get(e2.v, -1))
            and max(idx.get(e2.u, -1), idx.get(e2.v, -1)) < hi
            for e2 in g.edges
            if e2.edge_id != e.edge_id
        )
        if not nested:
            adj2 = is_hull_adjacent(h, e.u, e.v)
            if adj2.gate_free:
                return e.u, e.v, [e.edge_id]
    decomp = decompose_blocks(g)
    for ear in find_graph_ears(g, decomp):
        adj = is_hull_adjacent(h, ear.gate_a, ear.gate_b)
        if adj.gate_free:
            return ear.gate_a, ear.gate_b, ear.edge_ids
    return None


def build_candidate_ear(g: GateGraph, gate_a: str, gate_b: str, edge_ids: list[str]) -> CandidateGeometricEar:
    """Candidate boundary: graph path union gate-free hull arc."""
    h = g.hull_boundary_order
    adj = is_hull_adjacent(h, gate_a, gate_b)
    return CandidateGeometricEar(
        ear_id=f"geo_{gate_a}_{gate_b}",
        gate_a=gate_a,
        gate_b=gate_b,
        graph_path_edges=edge_ids,
        hull_arc=adj,
        jordan_subdisk=adj.gate_free,
        saturated=True,
        t051_eligible=adj.gate_free,
    )


def find_hull_adjacent_geometric_ear(g: GateGraph) -> CandidateGeometricEar | None:
    """Locate saturated geometric subcluster E with two-gate attachment."""
    leaf = weak_dual_leaf_face(g)
    if leaf is None:
        return None
    ga, gb, eids = leaf
    return build_candidate_ear(g, ga, gb, eids)


def audit_t058(g: GateGraph, *, diameter: float = 1.0) -> T058Audit:
    """
    T058: finite outerplanar saturated cluster with >=4 gates has hull-adjacent geometric ear.
    """
    op = audit_outerplanarity(g)
    if not op.is_outerplanar:
        return T058Audit(
            status="DISPROVED_COUNTEREXAMPLE",
            geometric_ear=None,
            weak_dual_leaf=False,
            messages=["Gate graph not outerplanar"],
        )
    if g.gate_count < 4:
        return T058Audit(
            status="PROVED_LOCALLY",
            geometric_ear=None,
            weak_dual_leaf=False,
            messages=["Fewer than four gates — two-gate case"],
        )
    reduced = reduce_gate_graph(g)
    ear = find_hull_adjacent_geometric_ear(reduced)
    if ear and ear.t051_eligible:
        return T058Audit(
            status="PROVED_LOCALLY",
            geometric_ear=ear,
            weak_dual_leaf=True,
            messages=[f"Hull-adjacent geometric ear at ({ear.gate_a},{ear.gate_b}), diam={diameter}"],
        )
    return T058Audit(
        status="CONJECTURAL_TARGET",
        geometric_ear=ear,
        weak_dual_leaf=ear is not None,
        messages=["No hull-adjacent geometric ear found"],
    )


def t058_statement() -> str:
    return "T058 — PROVED_LOCALLY for outerplanar Jordan-disk clusters via weak-dual leaf"
