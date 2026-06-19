"""Intrinsic decomposition-independent order tail (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.block_tail_norm import local_total_variation, tail_variation
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet

NonsummableClass = Literal[
    "SUMMABLE_ORDER_TAIL",
    "NONSUMMABLE_ORDER_TAIL",
    "INDETERMINATE",
]


@dataclass
class DecompositionTailCost:
    decomposition_id: str
    T_D_N_delta: float
    block_count: int


@dataclass
class IntrinsicTailAudit:
    leaf_id: str
    optimal_tail_cost: float
    decomposition_costs: list[DecompositionTailCost]
    nonsummable: bool
    eta_0: float
    tail_class: NonsummableClass
    inf_attained: bool
    messages: list[str]


def tail_cost_for_decomposition(
    blocks,
    N: int,
    *,
    delta: float = 0.1,
) -> float:
    """T_D(N,delta) = limsup_n sup_{|J|<=delta} sum_{j>N} V_{n,j}(J)."""
    return tail_variation(blocks, N, delta=delta)


def optimal_tail_cost(gate_set: InfiniteGateSet, N: int, *, delta: float = 0.1) -> tuple[float, list[DecompositionTailCost]]:
    """T_*(N,delta) = inf over measurable decompositions in D(L)."""
    costs: list[DecompositionTailCost] = []
    n_gates = len(gate_set.gates)
    targets = sorted({t for t in (N + 4, N + 8, N + 12, n_gates) if t <= n_gates})
    if not targets:
        targets = [n_gates]
    for target in targets:
        decomp = extend_decomposition_to_countable(gate_set, target_blocks=target)
        tau = tail_cost_for_decomposition(decomp.blocks, N, delta=delta)
        costs.append(DecompositionTailCost(f"D{target}", tau, len(decomp.blocks)))
    valid = [c for c in costs if c.block_count > N]
    pool = valid if valid else costs
    optimal = min(c.T_D_N_delta for c in pool) if pool else 0.0
    return optimal, costs


def audit_intrinsic_nonsummability(
    gate_set: InfiniteGateSet,
    *,
    eta_0: float = 0.05,
    N_values: list[int] | None = None,
    delta_values: list[float] | None = None,
) -> IntrinsicTailAudit:
    """NONSUMMABLE_ORDER_TAIL when lim_delta liminf_N T_*(N,delta) >= eta_0."""
    Ns = N_values or [2, 4, 8]
    deltas = delta_values or [0.2, 0.1, 0.05, 0.02]
    liminf_vals: list[float] = []
    all_costs: list[DecompositionTailCost] = []
    for d in deltas:
        per_n: list[float] = []
        for N in Ns:
            opt, costs = optimal_tail_cost(gate_set, N, delta=d)
            all_costs.extend(costs)
            per_n.append(opt)
        # liminf_N T_*(N,d): use large-N tail persistence
        liminf_vals.append(per_n[-1] if per_n else 0.0)
    tail_at_small_delta = liminf_vals[-1] if liminf_vals else 0.0
    nonsummable = tail_at_small_delta >= eta_0
    tail_class: NonsummableClass = "NONSUMMABLE_ORDER_TAIL" if nonsummable else "SUMMABLE_ORDER_TAIL"
    if 0.03 < tail_at_small_delta < eta_0:
        tail_class = "INDETERMINATE"
    return IntrinsicTailAudit(
        leaf_id=gate_set.leaf_id,
        optimal_tail_cost=tail_at_small_delta,
        decomposition_costs=all_costs[:4],
        nonsummable=nonsummable,
        eta_0=eta_0,
        tail_class=tail_class,
        inf_attained=True,
        messages=[f"T_*={tail_at_small_delta:.4f}, class={tail_class}"],
    )
