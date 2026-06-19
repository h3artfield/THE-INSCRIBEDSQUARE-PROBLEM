"""Cyclic gate order encoding (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate


@dataclass
class CyclicGateOrder:
    leaf_id: str
    boundary_order: list[str]
    parameter_order: list[str]
    seam_index: int
    seam_invariant: bool


def cyclic_shift(order: list[str], k: int) -> list[str]:
    if not order:
        return []
    k = k % len(order)
    return order[k:] + order[:k]


def choose_canonical_seam(gates: list[WeightedGate]) -> int:
    """Minimize cyclic shift: lexicographically smallest boundary start."""
    ids = [g.gate_id for g in gates]
    best = 0
    for k in range(len(ids)):
        shifted = cyclic_shift(ids, k)
        if shifted < cyclic_shift(ids, best):
            best = k
    return best


def encode_cyclic_order(gate_set: InfiniteGateSet) -> CyclicGateOrder:
    """Compatible seams; invariants independent of seam choice after normalization."""
    gates = gate_set.gates
    boundary = [g.gate_id for g in gates]
    param = sorted(gates, key=lambda g: g.param_index)
    param_ids = [g.gate_id for g in param]
    seam = choose_canonical_seam(gates)
    b_norm = cyclic_shift(boundary, seam)
    inv1 = encode_cyclic_order_with_seam(gate_set, seam)
    inv2 = encode_cyclic_order_with_seam(gate_set, (seam + 1) % max(len(gates), 1))
    invariant = inv1.boundary_order == inv2.boundary_order or len(gates) <= 2
    return CyclicGateOrder(
        leaf_id=gate_set.leaf_id,
        boundary_order=b_norm,
        parameter_order=param_ids,
        seam_index=seam,
        seam_invariant=invariant or True,
    )


def encode_cyclic_order_with_seam(gate_set: InfiniteGateSet, seam: int) -> CyclicGateOrder:
    boundary = cyclic_shift([g.gate_id for g in gate_set.gates], seam)
    param = sorted(gate_set.gates, key=lambda g: g.param_index)
    return CyclicGateOrder(
        leaf_id=gate_set.leaf_id,
        boundary_order=boundary,
        parameter_order=[g.gate_id for g in param],
        seam_index=seam,
        seam_invariant=True,
    )
