"""Canonical geometric ear peeling (Directive 030)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.block_decomposition import decompose_blocks
from squarepeg.defect_extraction.gate_graph import GateGraph
from squarepeg.defect_extraction.hull_adjacent_ear import (
    CandidateGeometricEar,
    find_hull_adjacent_geometric_ear,
    reduce_gate_graph,
)
from squarepeg.defect_extraction.geometric_ear import GraphEar

PeelStatus = Literal[
    "TWO_GATE_REMAINDER",
    "ALL_EARS_EXTRACTED",
    "TERMINATED",
]


@dataclass
class GeometricPeelStep:
    step: int
    ear: CandidateGeometricEar
    kappa_before: int
    kappa_after: int


@dataclass
class GeometricPeelingResult:
    status: PeelStatus
    steps: list[GeometricPeelStep]
    jordan_preserved: bool
    gate_ordered: bool
    messages: list[str] = field(default_factory=list)


def complexity_kappa(g: GateGraph, intrusion_nodes: int = 0) -> int:
    """kappa(C) = |V| + |E| + #intrusion nodes."""
    return g.gate_count + len(g.edges) + intrusion_nodes


def _remove_ear_edges(g: GateGraph, ear: CandidateGeometricEar) -> GateGraph:
    remaining = [e for e in g.edges if e.edge_id not in ear.graph_path_edges]
    active = {ear.gate_a, ear.gate_b}
    for e in remaining:
        active.add(e.u)
        active.add(e.v)
    verts = [v for v in g.vertices if v.gate_id in active]
    h = [gid for gid in g.hull_boundary_order if gid in active]
    return GateGraph(vertices=verts, edges=remaining, hull_boundary_order=h)


def _select_ear(g: GateGraph) -> CandidateGeometricEar | None:
    """Canonical order: weak-dual leaf, leaf block, smallest span, param tie-break."""
    ear = find_hull_adjacent_geometric_ear(g)
    if ear:
        return ear
    decomp = decompose_blocks(g)
    h = g.hull_boundary_order
    idx = {gid: i for i, gid in enumerate(h)}
    best: CandidateGeometricEar | None = None
    best_span = 10 ** 9
    for b in decomp.leaf_blocks:
        if len(b.vertices) != 2:
            continue
        ga, gb = b.vertices[0], b.vertices[1]
        span = abs(idx.get(ga, 0) - idx.get(gb, 0))
        if span < best_span:
            best_span = span
            from squarepeg.defect_extraction.hull_adjacent_ear import build_candidate_ear

            best = build_candidate_ear(g, ga, gb, b.edges)
    return best


def geometric_ear_peeling(
    g: GateGraph,
    *,
    intrusion_nodes: int = 0,
    max_steps: int = 64,
) -> GeometricPeelingResult:
    """Peel hull-adjacent geometric ears; kappa strictly decreases each step."""
    steps: list[GeometricPeelStep] = []
    current = reduce_gate_graph(g)
    kappa = complexity_kappa(current, intrusion_nodes)
    for step in range(max_steps):
        if current.gate_count <= 2 or not current.edges:
            return GeometricPeelingResult(
                status="TWO_GATE_REMAINDER" if current.gate_count <= 2 else "ALL_EARS_EXTRACTED",
                steps=steps,
                jordan_preserved=True,
                gate_ordered=True,
                messages=["Geometric peel complete"],
            )
        ear = _select_ear(current)
        if ear is None or not ear.t051_eligible:
            return GeometricPeelingResult(
                status="TERMINATED",
                steps=steps,
                jordan_preserved=False,
                gate_ordered=False,
                messages=["No T058 geometric ear"],
            )
        k_before = kappa
        current = _remove_ear_edges(current, ear)
        kappa = complexity_kappa(current, intrusion_nodes)
        steps.append(
            GeometricPeelStep(step=step, ear=ear, kappa_before=k_before, kappa_after=kappa)
        )
        if kappa >= k_before:
            break
    return GeometricPeelingResult(
        status="TERMINATED",
        steps=steps,
        jordan_preserved=True,
        gate_ordered=True,
        messages=["Max steps or kappa plateau"],
    )
