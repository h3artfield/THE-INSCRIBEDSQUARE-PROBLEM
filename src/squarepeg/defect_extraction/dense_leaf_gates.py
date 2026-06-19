"""Dense gate measures and inversion density (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

GateMeasureClass = Literal[
    "ATOMIC_ACCUMULATION",
    "DIFFUSE_BOUNDARY",
    "FINITE_ACCUMULATION_POINTS",
    "CANTOR_SUPPORT",
]


@dataclass
class LeafGateMeasure:
    leaf_id: str
    gate_count: int
    measure_class: GateMeasureClass
    atomic_mass_fraction: float
    inversion_density: float
    boundary_order_compatible: bool
    ordered_surgery_eligible: bool


def gate_measure_on_leaf(
    leaf_id: str,
    gate_positions: list[tuple[float, float]],
    param_order: list[int],
    *,
    leaf_closure_center: tuple[float, float] = (0.0, 0.0),
    leaf_radius: float = 0.5,
) -> LeafGateMeasure:
    """Classify nu_L gate measure on leaf boundary."""
    on_boundary = [
        i
        for i, p in enumerate(gate_positions)
        if _dist(p, leaf_closure_center) <= leaf_radius * 1.1
    ]
    count = len(on_boundary)
    measure: GateMeasureClass = "DIFFUSE_BOUNDARY"
    atomic_frac = 0.0
    if count <= 2:
        measure = "ATOMIC_ACCUMULATION"
        atomic_frac = 1.0 if count else 0.0
    elif count <= 8:
        measure = "FINITE_ACCUMULATION_POINTS"
        atomic_frac = 1.0 / count
    elif count > 20:
        measure = "CANTOR_SUPPORT" if _has_gaps(param_order, on_boundary) else "DIFFUSE_BOUNDARY"
    inv = _inversion_density(param_order, on_boundary)
    compatible = inv < 0.1
    ordered = count == 2 and compatible
    return LeafGateMeasure(
        leaf_id=leaf_id,
        gate_count=count,
        measure_class=measure,
        atomic_mass_fraction=atomic_frac,
        inversion_density=inv,
        boundary_order_compatible=compatible,
        ordered_surgery_eligible=ordered,
    )


def _inversion_density(param_order: list[int], indices: list[int]) -> float:
    if len(indices) < 2:
        return 0.0
    sub = [param_order[i] for i in sorted(indices) if i < len(param_order)]
    if len(sub) < 2:
        return 0.0
    inversions = 0
    pairs = 0
    for i, a in enumerate(sub):
        for b in sub[i + 1 :]:
            pairs += 1
            if a > b:
                inversions += 1
    return inversions / pairs if pairs else 0.0


def _has_gaps(param_order: list[int], indices: list[int]) -> bool:
    if len(indices) < 3:
        return False
    sub = sorted(param_order[i] for i in indices if i < len(param_order))
    gaps = sum(1 for i in range(len(sub) - 1) if sub[i + 1] - sub[i] > 3)
    return gaps >= len(sub) // 3


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
