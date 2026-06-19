"""Planar inversion graph for alternating order pairs (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet


@dataclass
class InversionEdge:
    i: int
    j: int
    weight: float


@dataclass
class PlanarInversionGraph:
    n_vertices: int
    edges: list[InversionEdge]
    edge_count: int
    planar: bool
    max_degree: int


@dataclass
class InversionGraphAudit:
    graph: PlanarInversionGraph
    crossing_free: bool
    superlinear_for_diffuse: bool
    messages: list[str]


def build_inversion_graph(gate_set: InfiniteGateSet) -> PlanarInversionGraph:
    """Auxiliary graph: edges = alternating-order gate pairs (inversions)."""
    perm = gate_permutation(gate_set)
    pi = perm.pi
    gates = gate_set.gates[: len(pi)]
    edges: list[InversionEdge] = []
    for i in range(len(pi)):
        for j in range(i + 1, len(pi)):
            if pi[i] > pi[j]:
                w = gates[i].scale_weight * gates[j].scale_weight if i < len(gates) and j < len(gates) else 1.0
                edges.append(InversionEdge(i, j, w))
    degrees = [0] * len(pi)
    for e in edges:
        degrees[e.i] += 1
        degrees[e.j] += 1
    n = len(pi)
    planar = len(edges) <= 3 * n - 6 if n >= 3 else True
    return PlanarInversionGraph(
        n_vertices=n,
        edges=edges,
        edge_count=len(edges),
        planar=planar,
        max_degree=max(degrees) if degrees else 0,
    )


def audit_inversion_graph_planarity(
    gate_set: InfiniteGateSet,
    *,
    depth: int = 8,
    branching: int = 4,
) -> InversionGraphAudit:
    """Planarity under bounded depth/branching constraints."""
    graph = build_inversion_graph(gate_set)
    n = graph.n_vertices
    linear_bound = depth * branching * n
    superlinear = graph.edge_count > linear_bound and n >= 6
    crossing_free = graph.planar and graph.max_degree <= depth * branching
    return InversionGraphAudit(
        graph=graph,
        crossing_free=crossing_free,
        superlinear_for_diffuse=superlinear,
        messages=[f"edges={graph.edge_count}, planar={graph.planar}, superlinear={superlinear}"],
    )
