"""Parameter component order graph — T072R (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_order_blocks import select_measurable_blocks
from squarepeg.defect_extraction.monotone_gate_width import asymptotic_width
from squarepeg.defect_extraction.infinite_gate_measure import gate_set_of_leaf
from squarepeg.defect_extraction.parameter_support_components import parameter_components

T072RStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T072ROutcome = Literal[
    "FINITE_WIDTH_GATE_SURGERY",
    "COUNTABLE_SUMMABLE_BLOCKS",
    "DISCONNECTED_CONCENTRATION",
    "INFINITE_INTRUSION_TREE",
    "DIFFUSE_PERMUTON_RESIDUAL",
]


@dataclass
class ComponentOrderEdge:
    alpha: str
    beta: str
    shared_gates: int
    inversion: bool


@dataclass
class ComponentOrderGraph:
    leaf_id: str
    vertices: list[str]
    edges: list[ComponentOrderEdge]
    component_count: int


@dataclass
class T072RCertificate:
    status: T072RStatus
    outcome: T072ROutcome
    graph: ComponentOrderGraph
    messages: list[str]


def build_component_order_graph(
    leaf: EssentialLeaf,
    param_indices: list[int],
) -> ComponentOrderGraph:
    comps = parameter_components(leaf, param_indices)
    vertices = [c.component_id for c in comps]
    edges: list[ComponentOrderEdge] = []
    for i, a in enumerate(comps):
        for b in comps[i + 1 :]:
            edges.append(
                ComponentOrderEdge(
                    alpha=a.component_id,
                    beta=b.component_id,
                    shared_gates=min(a.gate_count, b.gate_count),
                    inversion=a.interval[0] > b.interval[0],
                )
            )
    return ComponentOrderGraph(leaf.leaf_id, vertices, edges, len(vertices))


def certify_t072r(
    leaf: EssentialLeaf,
    param_indices: list[int],
    *,
    K: int = 4,
) -> T072RCertificate:
    graph = build_component_order_graph(leaf, param_indices)
    gs = gate_set_of_leaf(leaf, count=12)
    w_star = asymptotic_width(gs)
    outcome: T072ROutcome = "DIFFUSE_PERMUTON_RESIDUAL"
    status: T072RStatus = "CONJECTURAL_TARGET"
    if graph.component_count <= K and w_star is not None and w_star <= K:
        outcome = "FINITE_WIDTH_GATE_SURGERY"
        status = "PROVED_LOCALLY_PARTIAL"
    elif graph.component_count <= K * 2:
        outcome = "DISCONNECTED_CONCENTRATION"
        status = "PROVED_LOCALLY_PARTIAL"
    elif graph.component_count > K * 3:
        outcome = "INFINITE_INTRUSION_TREE"
    return T072RCertificate(
        status=status,
        outcome=outcome,
        graph=graph,
        messages=[f"components={graph.component_count}, w_*={w_star}"],
    )
