"""Recursive ear peeling (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.block_decomposition import decompose_blocks
from squarepeg.defect_extraction.gate_graph import GateGraph
from squarepeg.defect_extraction.geometric_ear import (
    GraphEar,
    T056Audit,
    audit_t056,
    ear_removal_confluence,
    validate_geometric_ear,
)

PeelStatus = Literal[
    "TWO_GATE_REMAINDER",
    "ALL_EARS_SURGERY",
    "IRREDUCIBLE_GRAPH",
    "GEOMETRIC_GAP",
]


@dataclass
class PeelStep:
    step: int
    ear: GraphEar
    geometric: bool
    remaining_gates: int


@dataclass
class EarPeelingResult:
    status: PeelStatus
    steps: list[PeelStep]
    confluence: str
    jordan_preserved: bool
    gate_ordered: bool
    messages: list[str] = field(default_factory=list)


def _remove_ear(g: GateGraph, ear: GraphEar) -> GateGraph:
    """Remove peeled ear edges; shrink gate set if isolated."""
    remaining_edges = [e for e in g.edges if e.edge_id not in ear.edge_ids]
    active = {ear.gate_a, ear.gate_b}
    for e in remaining_edges:
        active.add(e.u)
        active.add(e.v)
    verts = [v for v in g.vertices if v.gate_id in active]
    h_order = [gid for gid in g.hull_boundary_order if gid in active]
    from squarepeg.defect_extraction.gate_graph import GateGraph

    return GateGraph(vertices=verts, edges=remaining_edges, hull_boundary_order=h_order)


def peel_ears(g: GateGraph, *, max_steps: int = 32) -> EarPeelingResult:
    """
    Finite reduction: find two-gate ear, peel, resaturate remainder, repeat.

    Canonical order: smallest leaf block (innermost) first.
    """
    steps: list[PeelStep] = []
    current = g
    for step in range(max_steps):
        if current.gate_count <= 2:
            return EarPeelingResult(
                status="TWO_GATE_REMAINDER",
                steps=steps,
                confluence=ear_removal_confluence(),
                jordan_preserved=True,
                gate_ordered=True,
                messages=["Reduced to two-gate cluster"],
            )
        decomp = decompose_blocks(current)
        t056 = audit_t056(current, decomp)
        if not t056.graph_ears:
            return EarPeelingResult(
                status="IRREDUCIBLE_GRAPH",
                steps=steps,
                confluence=ear_removal_confluence(),
                jordan_preserved=True,
                gate_ordered=False,
                messages=t056.messages + ["No graph ear found"],
            )
        ear = sorted(t056.graph_ears, key=lambda e: (len(e.edge_ids), e.gate_a))[0]
        geo = validate_geometric_ear(current, ear)
        steps.append(
            PeelStep(
                step=step,
                ear=ear,
                geometric=geo.retained_disjoint and geo.crosscut_admits,
                remaining_gates=current.gate_count,
            )
        )
        if not geo.retained_disjoint:
            return EarPeelingResult(
                status="GEOMETRIC_GAP",
                steps=steps,
                confluence=ear_removal_confluence(),
                jordan_preserved=False,
                gate_ordered=False,
                messages=["Graph ear lacks geometric isolation"],
            )
        current = _remove_ear(current, ear)
        if not current.edges:
            return EarPeelingResult(
                status="ALL_EARS_SURGERY",
                steps=steps,
                confluence=ear_removal_confluence(),
                jordan_preserved=True,
                gate_ordered=True,
                messages=["All ears marked for cluster surgery"],
            )
    return EarPeelingResult(
        status="IRREDUCIBLE_GRAPH",
        steps=steps,
        confluence=ear_removal_confluence(),
        jordan_preserved=True,
        gate_ordered=False,
        messages=["Max peel steps exceeded"],
    )
