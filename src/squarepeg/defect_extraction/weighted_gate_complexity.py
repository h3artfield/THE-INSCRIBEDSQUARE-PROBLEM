"""Weighted gate complexity G(L) (Directive 035)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_extraction.infinite_gate_measure import (
    InfiniteGateSet,
    WeightedGate,
    complexity_weight,
)
from squarepeg.defect_extraction.finite_gate_truncation import GateTruncation, finite_gate_truncation


JOIN_CONSTANT = 4.5


@dataclass
class WeightedComplexity:
    leaf_id: str
    total_complexity: float
    tail_complexity: float
    pair_integral: float
    scale_decomposition: list[tuple[int, float, float]]


def gate_complexity_functional(gate_set: InfiniteGateSet) -> WeightedComplexity:
    """
    G(L) = sum_j M_j^2 r_j^2 over canonical scale decomposition.
    Equivalent pair formulation: iint s(g)s(h) dnu dnu (derived from join bound).
    """
    scales = _scale_decomposition(gate_set.gates)
    pair_sum = 0.0
    for i, gi in enumerate(gate_set.gates):
        for gj in gate_set.gates[i + 1 :]:
            pair_sum += complexity_weight(gi, gj)
    decomp_sum = sum(m * m * r * r for m, r, _ in scales)
    total = max(pair_sum, decomp_sum)
    return WeightedComplexity(
        leaf_id=gate_set.leaf_id,
        total_complexity=total,
        tail_complexity=0.0,
        pair_integral=pair_sum,
        scale_decomposition=[(m, r, m * r) for m, r, _ in scales],
    )


def tail_complexity(gate_set: InfiniteGateSet, trunc: GateTruncation) -> float:
    """G_N^tail(L) -> 0 as N -> infty."""
    full = gate_complexity_functional(gate_set)
    sub = gate_set_of_truncation(gate_set, trunc)
    sub_c = gate_complexity_functional(sub)
    return max(full.total_complexity - sub_c.total_complexity, 0.0)


def gate_set_of_truncation(full: InfiniteGateSet, trunc: GateTruncation) -> InfiniteGateSet:
    return InfiniteGateSet(
        leaf_id=full.leaf_id,
        gate_class="FINITE",
        gates=trunc.gates,
        closed=True,
        total_mass=sum(g.scale_weight for g in trunc.gates),
    )


def _scale_decomposition(gates: list[WeightedGate]) -> list[tuple[int, float, float]]:
    if not gates:
        return []
    buckets: dict[int, list[WeightedGate]] = {}
    for g in gates:
        bucket = int(round(-math.log10(max(g.scale_weight, 1e-6))))
        buckets.setdefault(bucket, []).append(g)
    result: list[tuple[int, float, float]] = []
    for _, grp in sorted(buckets.items()):
        m = len(grp)
        r = sum(g.scale_weight for g in grp) / m
        result.append((m, r, m * r))
    return result
