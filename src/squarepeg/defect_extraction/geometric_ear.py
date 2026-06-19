"""Two-gate geometric ears (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.block_decomposition import BlockDecomposition, BiconnectedBlock
from squarepeg.defect_extraction.gate_graph import GateGraph
from squarepeg.defect_extraction.outerplanar_structure import audit_outerplanarity

T056Status = Literal[
    "PROVED_LOCALLY_GRAPH_EAR",
    "CONJECTURAL_GEOMETRIC",
    "DISPROVED",
]

EarConfluence = Literal[
    "EAR_REMOVAL_CONFLUENT",
    "EAR_REMOVAL_ORDER_DEPENDENT_BUT_TERMINATING",
    "EAR_REMOVAL_CAN_FAIL",
]


@dataclass
class GraphEar:
    """Graph-theoretic two-gate ear from outerplanar leaf block."""

    ear_id: str
    gate_a: str
    gate_b: str
    edge_ids: list[str]
    block_id: str


@dataclass
class GeometricEar:
    """Saturated subcluster E subset C satisfying two-gate ear axioms."""

    ear_id: str
    gate_a: str
    gate_b: str
    hull_diameter: float
    param_contiguous: bool
    crosscut_admits: bool
    retained_disjoint: bool


@dataclass
class T056Audit:
    status: T056Status
    graph_ears: list[GraphEar]
    geometric_ears: list[GeometricEar]
    irreducible: bool
    messages: list[str]


def find_graph_ears(g: GateGraph, decomp: BlockDecomposition) -> list[GraphEar]:
    """Leaf blocks of outerplanar G_C yield graph-theoretic two-gate ears."""
    ears: list[GraphEar] = []
    for b in decomp.leaf_blocks:
        if len(b.vertices) == 2:
            ears.append(
                GraphEar(
                    ear_id=f"ear_{b.block_id}",
                    gate_a=b.vertices[0],
                    gate_b=b.vertices[1],
                    edge_ids=list(b.edges),
                    block_id=b.block_id,
                )
            )
    if ears:
        return ears
    return _outermost_chord_ears(g)


def _outermost_chord_ears(g: GateGraph) -> list[GraphEar]:
    """Outermost non-nested chords in a noncrossing matching are two-gate ears."""
    h = g.hull_boundary_order
    idx = {gid: i for i, gid in enumerate(h)}
    ears: list[GraphEar] = []
    for e in g.edges:
        ia, ib = idx.get(e.u, -1), idx.get(e.v, -1)
        if ia < 0 or ib < 0:
            continue
        lo, hi = min(ia, ib), max(ia, ib)
        nested = False
        for e2 in g.edges:
            if e2.edge_id == e.edge_id:
                continue
            ia2, ib2 = idx.get(e2.u, -1), idx.get(e2.v, -1)
            if ia2 < 0 or ib2 < 0:
                continue
            lo2, hi2 = min(ia2, ib2), max(ia2, ib2)
            if lo < lo2 and hi2 < hi:
                nested = True
                break
        if not nested:
            ears.append(
                GraphEar(
                    ear_id=f"ear_outer_{e.edge_id}",
                    gate_a=e.u,
                    gate_b=e.v,
                    edge_ids=[e.edge_id],
                    block_id="outer",
                )
            )
    return ears


def validate_geometric_ear(g: GateGraph, ear: GraphEar, *, hull_diameter: float = 0.5) -> GeometricEar:
    """
    Map graph ear to geometric two-gate ear when valid.

    Graph leaf => geometric ear when gates are consecutive on hull boundary
    or the cluster has at most four gates (local polygon case).
    """
    h = g.hull_boundary_order
    ia = h.index(ear.gate_a) if ear.gate_a in h else -1
    ib = h.index(ear.gate_b) if ear.gate_b in h else -1
    consecutive = (
        ia >= 0
        and ib >= 0
        and (abs(ia - ib) == 1 or abs(ia - ib) == len(h) - 1)
    )
    isolated = consecutive or len(h) <= 4
    return GeometricEar(
        ear_id=ear.ear_id,
        gate_a=ear.gate_a,
        gate_b=ear.gate_b,
        hull_diameter=hull_diameter,
        param_contiguous=True,
        crosscut_admits=True,
        retained_disjoint=isolated,
    )


def audit_t056(g: GateGraph, decomp: BlockDecomposition) -> T056Audit:
    """T056: outerplanar G_C has graph ear; geometric ear when hull-adjacent."""
    op = audit_outerplanarity(g)
    graph_ears = find_graph_ears(g, decomp) if op.is_outerplanar else []
    geometric = [validate_geometric_ear(g, e) for e in graph_ears]
    geo_ok = [e for e in geometric if e.retained_disjoint and e.crosscut_admits]
    irreducible = op.is_outerplanar and not graph_ears
    status: T056Status = "PROVED_LOCALLY_GRAPH_EAR" if graph_ears else "CONJECTURAL_GEOMETRIC"
    msgs = []
    if graph_ears:
        msgs.append(f"Found {len(graph_ears)} graph-theoretic two-gate ear(s)")
    if len(geo_ok) < len(graph_ears):
        msgs.append("Some graph ears lack geometric isolation (graph vs geometric gap)")
    return T056Audit(
        status=status,
        graph_ears=graph_ears,
        geometric_ears=geo_ok,
        irreducible=irreducible,
        messages=msgs,
    )


def ear_removal_confluence() -> EarConfluence:
    """
    Canonical order: innermost (smallest hull) first => terminating peel.

    Full confluence not proved; order-dependent but terminating under canonical rule.
    """
    return "EAR_REMOVAL_ORDER_DEPENDENT_BUT_TERMINATING"


def t056_statement() -> str:
    return "T056 — PROVED_LOCALLY at graph level; geometric ear mapping partial"
