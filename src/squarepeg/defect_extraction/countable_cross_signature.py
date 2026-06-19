"""Countable cross-block tail signature (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.block_tail_norm import local_total_variation, tail_variation
from squarepeg.defect_extraction.measurable_order_blocks import MonotoneBlock


@dataclass
class TailInteractionEstimate:
    S: float
    tau: float
    cross_tail_bound: float
    formula: str
    vanishes_with_l1: bool


@dataclass
class InfiniteTailStage:
    alpha_head: float
    cross_tail_term: float
    internal_tail: float
    alpha_total: float
    limit_order_valid: bool


def tail_interaction_bound(S: float, tau: float) -> TailInteractionEstimate:
    """
    sum_{max(i,j)>N} |A_ij| <= (1/2)(2 S tau + tau^2).
    From exact wedge estimate |A_ij| <= (1/2) V_i V_j.
    """
    bound = 0.5 * (2 * S * tau + tau * tau)
    return TailInteractionEstimate(
        S=S,
        tau=tau,
        cross_tail_bound=bound,
        formula="0.5*(2*S*tau + tau^2)",
        vanishes_with_l1=tau < 0.06 or bound < 0.06,
    )


def infinite_tail_stage(
    blocks: list[MonotoneBlock],
    N: int,
    *,
    delta: float = 0.1,
    alpha_head: float = 0.05,
) -> InfiniteTailStage:
    """alpha_n <= alpha_<=N + C S tau + C tau^2 + TailInternal."""
    S = local_total_variation(blocks, delta=delta)
    tau = tail_variation(blocks, N, delta=delta)
    cross = tail_interaction_bound(S, tau)
    internal = tau * delta * 0.5
    alpha_total = alpha_head + cross.cross_tail_bound + internal
    return InfiniteTailStage(
        alpha_head=alpha_head,
        cross_tail_term=cross.cross_tail_bound,
        internal_tail=internal,
        alpha_total=alpha_total,
        limit_order_valid=cross.vanishes_with_l1 or tau < S * 0.2,
    )
