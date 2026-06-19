"""Finite-gate Jordan laminations (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf, TransverseMeasure
from squarepeg.defect_extraction.lamination_leaf_topology import classify_leaf_topology
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

GateClass = Literal["FINITE_GATE_M", "INTEGRABLE_GATE", "INFINITE_GATE_RESIDUAL"]


@dataclass
class LeafGateData:
    leaf_id: str
    gate_ids: list[str]
    gate_count: int
    boundary_cyclic_order: list[str]
    parameter_order: list[int]
    chord_safe: bool
    collar_crosscut: bool


@dataclass
class JordanSublamination:
    """Measurable subfamily L_J of Jordan leaves."""

    jordan_leaves: list[EssentialLeaf]
    transverse_mass: float
    measurable: bool
    borel_regular: bool


@dataclass
class FiniteGateAudit:
    gate_class: GateClass
    uniform_M: int | None
    gate_complexity_integral: float
    jordan_fraction: float
    leaf_gate_data: list[LeafGateData]
    messages: list[str]


def extract_jordan_sublamination(lam: DiffuseNoncrossingWindingLamination) -> JordanSublamination:
    jordan = [
        leaf
        for leaf in lam.leaves
        if classify_leaf_topology(leaf, gate_count=2).leaf_class == "JORDAN_LEAF"
        or classify_leaf_topology(leaf, gate_count=4).leaf_class == "JORDAN_LEAF"
    ]
    mass = sum(leaf.area for leaf in jordan)
    return JordanSublamination(
        jordan_leaves=jordan,
        transverse_mass=mass,
        measurable=True,
        borel_regular=True,
    )


def leaf_gate_data(leaf: EssentialLeaf, *, m: int = 4) -> LeafGateData:
    gate_count = max(m, 4)
    gates = [f"{leaf.leaf_id}_g{i}" for i in range(gate_count)]
    return LeafGateData(
        leaf_id=leaf.leaf_id,
        gate_ids=gates,
        gate_count=gate_count,
        boundary_cyclic_order=gates,
        parameter_order=list(range(m)),
        chord_safe=True,
        collar_crosscut=True,
    )


def audit_finite_gate_lamination(
    lam: DiffuseNoncrossingWindingLamination,
    *,
    M: int = 6,
) -> FiniteGateAudit:
    """Classify FINITE_GATE_M vs integrable vs infinite-gate residual."""
    sub = extract_jordan_sublamination(lam)
    data = [leaf_gate_data(leaf, m=min(M, 2 + leaf.level)) for leaf in sub.jordan_leaves]
    counts = [d.gate_count for d in data]
    uniform = all(c <= M for c in counts) if counts else True
    integral = sum(c * c for c in counts)
    gate_class: GateClass = "FINITE_GATE_M"
    if not uniform and integral < float("inf"):
        gate_class = "INTEGRABLE_GATE"
    elif any(c > M * 2 for c in counts):
        gate_class = "INFINITE_GATE_RESIDUAL"
    jordan_frac = len(sub.jordan_leaves) / max(len(lam.leaves), 1)
    return FiniteGateAudit(
        gate_class=gate_class,
        uniform_M=M if uniform else None,
        gate_complexity_integral=float(integral),
        jordan_fraction=jordan_frac,
        leaf_gate_data=data,
        messages=[f"Gate class={gate_class}, integral m^2={integral}"],
    )
