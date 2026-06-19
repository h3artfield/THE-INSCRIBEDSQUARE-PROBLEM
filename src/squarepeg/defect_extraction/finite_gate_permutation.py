"""Finite gate permutations and inversion density (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.cyclic_gate_order import CyclicGateOrder, encode_cyclic_order
from squarepeg.defect_extraction.gate_inversion_energy import inversion_energy
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate


@dataclass
class GatePermutation:
    leaf_id: str
    N: int
    pi: list[int]
    inv_density: float
    inv_weighted: float
    converges_to_measure: bool


def permutation_from_orders(order: CyclicGateOrder) -> list[int]:
    """pi_N in S_N: parameter rank of gate at boundary position i."""
    b_idx = {gid: i for i, gid in enumerate(order.boundary_order)}
    p_rank = {gid: i for i, gid in enumerate(order.parameter_order)}
    return [p_rank[gid] for gid in order.boundary_order]


def inv_density(pi: list[int]) -> float:
    """Inv(pi_N) = 2/(N(N-1)) #{i<j : pi(i) > pi(j)}."""
    n = len(pi)
    if n < 2:
        return 0.0
    inv = sum(1 for i in range(n) for j in range(i + 1, n) if pi[i] > pi[j])
    return 2.0 * inv / (n * (n - 1))


def inv_weighted(pi: list[int], weights: list[float]) -> float:
    """Inv_nu(pi_N) = sum_{i<j} w_i w_j 1[pi(i) > pi(j)]."""
    total = 0.0
    for i in range(len(pi)):
        for j in range(i + 1, len(pi)):
            if pi[i] > pi[j]:
                total += weights[i] * weights[j]
    return total


def gate_permutation(gate_set: InfiniteGateSet, N: int | None = None) -> GatePermutation:
    n = N or len(gate_set.gates)
    sub = gate_set.gates[:n]
    from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet as IGS

    sub_set = IGS(gate_set.leaf_id, "FINITE", sub, True, sum(g.scale_weight for g in sub))
    order = encode_cyclic_order(sub_set)
    pi = permutation_from_orders(order)
    weights = [g.scale_weight for g in sub]
    inv_d = inv_density(pi)
    inv_w = inv_weighted(pi, weights)
    measure_inv = inversion_energy(sub_set).energy
    converges = abs(inv_d - measure_inv) < 0.15 or n < 4
    return GatePermutation(
        leaf_id=gate_set.leaf_id,
        N=n,
        pi=pi,
        inv_density=inv_d,
        inv_weighted=inv_w,
        converges_to_measure=converges,
    )


def longest_decreasing_subsequence(pi: list[int]) -> int:
    """LDS length for Dilworth/Mirsky width relation."""
    if not pi:
        return 0
    dp = [1] * len(pi)
    for i in range(len(pi)):
        for j in range(i):
            if pi[j] > pi[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
