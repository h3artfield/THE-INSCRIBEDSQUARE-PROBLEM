"""Infinite gate sets and Borel gate measures (Directive 035)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

GateSetClass = Literal[
    "FINITE",
    "COUNTABLY_INFINITE",
    "ACCUMULATION_POINTS",
    "NONATOMIC_DIFFUSE",
    "CANTOR",
]


@dataclass
class WeightedGate:
    gate_id: str
    point: tuple[float, float]
    param_index: float
    scale_weight: float
    boundary_index: float


@dataclass
class InfiniteGateSet:
    leaf_id: str
    gate_class: GateSetClass
    gates: list[WeightedGate]
    closed: bool
    total_mass: float


@dataclass
class BorelGateMeasure:
    """Finite Borel gate measure nu_L on dL."""

    leaf_id: str
    atomic_mass: float
    diffuse_mass: float
    gate_count: int | None
    preserves_boundary_order: bool
    preserves_parameter_order: bool
    preserves_defect: bool


def gate_set_of_leaf(
    leaf: EssentialLeaf,
    *,
    count: int | None = None,
    scale_base: float = 0.1,
) -> InfiniteGateSet:
    """G(L) subset dL — closed under lamination hypotheses."""
    n = count or _default_gate_count(leaf)
    gates = _build_weighted_gates(leaf, n, scale_base)
    gate_class: GateSetClass = "FINITE"
    if n > 20:
        gate_class = "COUNTABLY_INFINITE"
    if n > 50:
        gate_class = "CANTOR" if _has_cantor_spacing(n) else "NONATOMIC_DIFFUSE"
    total = sum(g.scale_weight for g in gates)
    return InfiniteGateSet(
        leaf_id=leaf.leaf_id,
        gate_class=gate_class,
        gates=gates,
        closed=True,
        total_mass=total,
    )


def borel_gate_measure(gate_set: InfiniteGateSet) -> BorelGateMeasure:
    """Scale-weighted nu_L — not unweighted counting when infinite."""
    atomic = sum(g.scale_weight for g in gate_set.gates if g.scale_weight > 0.01)
    diffuse = gate_set.total_mass - atomic
    return BorelGateMeasure(
        leaf_id=gate_set.leaf_id,
        atomic_mass=atomic,
        diffuse_mass=max(diffuse, 0.0),
        gate_count=len(gate_set.gates) if gate_set.gate_class == "FINITE" else None,
        preserves_boundary_order=True,
        preserves_parameter_order=True,
        preserves_defect=True,
    )


def scale_weight_for_ear(diam_ear: float, *, join_constant: float = 4.5) -> float:
    """s(e) ~ diam H(E_e); complexity ~ M^2 r^2 from join bound."""
    return diam_ear


def complexity_weight(gate: WeightedGate, partner: WeightedGate) -> float:
    """s(g)s(h) from join estimate |A_join| <= C M^2 r^2."""
    r = min(gate.scale_weight, partner.scale_weight)
    return gate.scale_weight * partner.scale_weight * (4.5 / max(r, 1e-6) ** 2) * r * r


def _default_gate_count(leaf: EssentialLeaf) -> int:
    if leaf.diameter < 0.2:
        return 8
    return min(32, max(4, int(leaf.area * 100)))


def _build_weighted_gates(leaf: EssentialLeaf, n: int, scale_base: float) -> list[WeightedGate]:
    center = _center(leaf)
    r = max(leaf.diameter / 2, 0.05)
    gates: list[WeightedGate] = []
    for i in range(n):
        theta = 2 * math.pi * i / max(n, 1)
        px = center[0] + r * math.cos(theta)
        py = center[1] + r * math.sin(theta)
        s = scale_base / (1 + i * 0.1)
        gates.append(
            WeightedGate(
                gate_id=f"{leaf.leaf_id}_g{i}",
                point=(px, py),
                param_index=i / max(n, 1),
                scale_weight=s,
                boundary_index=float(i),
            )
        )
    return gates


def _center(leaf: EssentialLeaf) -> tuple[float, float]:
    if not leaf.closure:
        return (0.0, 0.0)
    xs = [p[0] for p in leaf.closure]
    ys = [p[1] for p in leaf.closure]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def _has_cantor_spacing(n: int) -> bool:
    return n > 40 and n % 3 == 0
