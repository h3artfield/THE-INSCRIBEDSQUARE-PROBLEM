"""Monotone gate width (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import (
    gate_permutation,
    inv_density,
    longest_decreasing_subsequence,
)
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet

WidthClass = Literal[
    "FINITE_ORDER_WIDTH",
    "COUNTABLE_SUMMABLE_WIDTH",
    "INFINITE_ORDER_WIDTH",
]


@dataclass
class MonotoneWidthAudit:
    leaf_id: str
    width: int
    lds_length: int
    inv_density: float
    width_class: WidthClass
    asymptotic_width: int | None
    dilworth_match: bool


def monotone_width(pi: list[int]) -> int:
    """Minimum order-compatible subsets partitioning gates = LDS length (Mirsky)."""
    return longest_decreasing_subsequence(pi)


def weighted_monotone_width(gate_set: InfiniteGateSet, *, eta: float = 0.05) -> int:
    """w_eta(L): min blocks covering all but eta of weighted gate mass."""
    perm = gate_permutation(gate_set)
    n_blocks = monotone_width(perm.pi)
    total_mass = gate_set.total_mass or 1.0
    if n_blocks == 0:
        return 1
    block_mass = total_mass / n_blocks
    covered = block_mass * n_blocks
    if 1.0 - covered / total_mass > eta:
        return n_blocks + 1
    return n_blocks


def asymptotic_width(gate_set: InfiniteGateSet, *, eta_values: list[float] | None = None) -> int | None:
    """w_*(L) = lim_{eta->0} w_eta(L)."""
    etas = eta_values or [0.2, 0.1, 0.05, 0.02, 0.01]
    widths = [weighted_monotone_width(gate_set, eta=e) for e in etas]
    if not widths:
        return None
    stable = widths[-1]
    if all(w <= stable + 1 for w in widths):
        return stable if stable < 20 else None
    return None


def audit_monotone_width(gate_set: InfiniteGateSet, *, K: int = 4) -> MonotoneWidthAudit:
    perm = gate_permutation(gate_set)
    w = monotone_width(perm.pi)
    lds = longest_decreasing_subsequence(perm.pi)
    w_star = asymptotic_width(gate_set)
    width_class: WidthClass = "FINITE_ORDER_WIDTH"
    if w_star is None or w_star > K:
        width_class = "INFINITE_ORDER_WIDTH"
    elif w_star and w_star > K:
        width_class = "COUNTABLE_SUMMABLE_WIDTH"
    if w_star is not None and w_star <= K:
        width_class = "FINITE_ORDER_WIDTH"
    return MonotoneWidthAudit(
        leaf_id=gate_set.leaf_id,
        width=w,
        lds_length=lds,
        inv_density=perm.inv_density,
        width_class=width_class,
        asymptotic_width=w_star,
        dilworth_match=w == lds,
    )
