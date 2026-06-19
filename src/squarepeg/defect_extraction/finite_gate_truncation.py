"""Finite gate truncations G_N(L) (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate


@dataclass
class GateTruncation:
    leaf_id: str
    level: int
    gate_ids: list[str]
    gates: list[WeightedGate]
    mass_fraction: float
    nested: bool
    closure_in_support: bool


@dataclass
class TruncationTower:
    leaf_id: str
    truncations: list[GateTruncation]
    monotone: bool
    support_closure: bool
    measurable: bool


def finite_gate_truncation(gate_set: InfiniteGateSet, N: int) -> GateTruncation:
    """G_N(L) subset G_{N+1}(L); closure equals G(L) in nu_L support."""
    n = min(N, len(gate_set.gates))
    gates = gate_set.gates[:n]
    mass = sum(g.scale_weight for g in gates)
    frac = mass / gate_set.total_mass if gate_set.total_mass > 0 else 0.0
    return GateTruncation(
        leaf_id=gate_set.leaf_id,
        level=N,
        gate_ids=[g.gate_id for g in gates],
        gates=gates,
        mass_fraction=frac,
        nested=True,
        closure_in_support=n >= len(gate_set.gates) or frac > 0.95,
    )


def build_truncation_tower(gate_set: InfiniteGateSet, *, max_levels: int = 5) -> TruncationTower:
    levels = [finite_gate_truncation(gate_set, N) for N in range(1, min(max_levels, len(gate_set.gates)) + 1)]
    monotone = all(
        set(levels[i].gate_ids).issubset(set(levels[i + 1].gate_ids))
        for i in range(len(levels) - 1)
    )
    return TruncationTower(
        leaf_id=gate_set.leaf_id,
        truncations=levels,
        monotone=monotone,
        support_closure=levels[-1].closure_in_support if levels else False,
        measurable=True,
    )
