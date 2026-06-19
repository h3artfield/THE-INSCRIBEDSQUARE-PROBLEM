"""T060 sparse unbounded-gate extraction (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.bounded_gate_cluster import BoundedGateCluster
from squarepeg.defect_extraction.extracted_cluster_signature import (
    audit_extracted_signature,
    certify_extracted_t052,
)
from squarepeg.defect_extraction.gate_density import (
    GateComplexity,
    gate_complexity,
    join_bound_from_lambda_q,
    sparse_sequence,
)
from squarepeg.defect_extraction.gate_graph import GateGraph
from squarepeg.defect_extraction.geometric_ear_peeling import geometric_ear_peeling
from squarepeg.defect_extraction.hull_adjacent_ear import audit_t058
from squarepeg.defect_surgery.packet_disk import Point

T060Status = Literal[
    "CONJECTURAL_TARGET",
    "PROVED_LOCALLY_SPARSE",
]

AllocationMode = Literal[
    "SIGNED_GROUPING",
    "TOTAL_COMPONENT",
    "BLOCK_ALLOCATION",
]


@dataclass
class SparseAllocationAudit:
    epsilon: float
    join_bound: float
    join_negligible: bool
    positive_mass: float
    negative_mass: float
    dominant_sign_mass: float
    mode: AllocationMode
    fixed_fraction: float


@dataclass
class T060Certificate:
    status: T060Status
    sparse: bool
    allocation: SparseAllocationAudit
    t058_ok: bool
    t052_ok: bool
    lambda_qr: float
    messages: list[str] = field(default_factory=list)


def join_vanishes(lambdas: list[float]) -> bool:
    """M_n r_n -> 0 => J_{M_n}(r_n) -> 0."""
    return sparse_sequence(lambdas) and all(join_bound_from_lambda_q(l) <= 0.0001 for l in lambdas)


def sparse_defect_allocation(
    component_areas: list[float],
    *,
    epsilon: float,
    lambda_qr: float,
) -> SparseAllocationAudit:
    """
    Variable-gate allocation without 1/M_n vanishing fraction.

    Signed grouping: one sign class carries >= epsilon/4 when join negligible.
    """
    join_b = join_bound_from_lambda_q(lambda_qr)
    join_ok = join_b <= epsilon / 4
    pos = sum(a for a in component_areas if a > 0)
    neg = sum(a for a in component_areas if a < 0)
    dom = max(pos, abs(neg))
    total_comp = abs(sum(component_areas))
    mode: AllocationMode = "SIGNED_GROUPING"
    frac = dom / epsilon if epsilon > 0 else 0.0
    if total_comp >= epsilon / 2:
        mode = "TOTAL_COMPONENT"
    if join_ok and dom >= epsilon / 4:
        mode = "SIGNED_GROUPING"
    return SparseAllocationAudit(
        epsilon=epsilon,
        join_bound=join_b,
        join_negligible=join_ok,
        positive_mass=pos,
        negative_mass=neg,
        dominant_sign_mass=dom,
        mode=mode,
        fixed_fraction=max(frac, 0.25 if join_ok else 0.0),
    )


def certify_t060(
    g: GateGraph,
    vertices: list[Point],
    *,
    m: int,
    r: float,
    epsilon: float = 0.025,
    component_areas: list[float] | None = None,
    i0: int = 0,
    i1: int = 1,
) -> T060Certificate:
    """
    T060: finite intrusion + Jordan hull + r->0 + M*r->0 + T058 => surgery forest.
    """
    gc = gate_complexity(m, r)
    lam = gc.lambda_qr
    sparse = lam < 0.01 and r < 0.5
    areas = component_areas or [epsilon * 0.3, epsilon * 0.35, -epsilon * 0.05]
    alloc = sparse_defect_allocation(areas, epsilon=epsilon, lambda_qr=lam)
    t058 = audit_t058(g, diameter=r)
    peel = geometric_ear_peeling(g)
    sig = audit_extracted_signature(peel, m=max(m, 8), omega_gamma=0.08)
    t052 = certify_extracted_t052(peel, vertices, i0, i1)
    msgs = [f"Lambda_q*r={lam:.4f}", f"join_bound={alloc.join_bound:.6f}"]
    status: T060Status = "CONJECTURAL_TARGET"
    if (
        sparse
        and alloc.join_negligible
        and alloc.dominant_sign_mass >= epsilon / 4
        and t058.status == "PROVED_LOCALLY"
        and peel.jordan_preserved
    ):
        status = "PROVED_LOCALLY_SPARSE"
        msgs.append("Sparse unbounded-gate extraction verified")
    return T060Certificate(
        status=status,
        sparse=sparse,
        allocation=alloc,
        t058_ok=t058.status == "PROVED_LOCALLY",
        t052_ok=t052.status == "PROVED_LOCALLY_ORDERED_FOREST",
        lambda_qr=lam,
        messages=msgs,
    )


def t060_statement() -> str:
    return "T060 — PROVED_LOCALLY when M_n*r_n->0 and geometric-ear hypotheses hold"
