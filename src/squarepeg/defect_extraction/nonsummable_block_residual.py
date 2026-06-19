"""NONSUMMABLE_ORDER_BLOCK_LAMINATION residual (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.block_tail_norm import audit_l1_block_signature, tail_variation
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet

TailOutcome = Literal[
    "T064D_CONCENTRATION",
    "T062_FINITE_CENTER",
    "INFINITE_INTRUSION_TREE",
    "DIFFUSE_PERMUTON",
    "INFINITE_CENTER",
    "NONSUMMABLE_RESIDUAL",
]


@dataclass
class NonsummableBlockAudit:
    is_nonsummable: bool
    tail_persistently_positive: bool
    outcome: TailOutcome
    messages: list[str]


def audit_nonsummable_tail(
    gate_set: InfiniteGateSet,
    *,
    delta: float = 0.1,
) -> NonsummableBlockAudit:
    decomp = extend_decomposition_to_countable(gate_set, target_blocks=16)
    blocks = decomp.blocks
    l1 = audit_l1_block_signature(blocks)
    tau = tail_variation(blocks, len(blocks) // 2, delta=delta) if len(blocks) > 2 else 0
    nonsummable = not l1.satisfies_l1 and tau > 0.1
    outcome: TailOutcome = "NONSUMMABLE_RESIDUAL"
    if nonsummable and tau > 0.5:
        outcome = "INFINITE_INTRUSION_TREE"
    elif nonsummable:
        outcome = "DIFFUSE_PERMUTON"
    return NonsummableBlockAudit(
        is_nonsummable=nonsummable,
        tail_persistently_positive=tau > 0.05,
        outcome=outcome,
        messages=[f"nonsummable={nonsummable}, tau={tau:.4f}"],
    )
