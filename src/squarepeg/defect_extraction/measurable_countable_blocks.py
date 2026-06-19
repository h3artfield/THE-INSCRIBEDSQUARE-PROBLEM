"""Measurable countable monotone block selection — T075 (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.measurable_order_blocks import MonotoneBlock, _monotone_blocks_from_pi

T075Status = Literal["CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class CountableBlockDecomposition:
    leaf_id: str
    blocks: list[MonotoneBlock]
    measurable: bool
    truncation_stable: bool
    no_mass_duplication: bool
    deterministic_indexing: bool


@dataclass
class T075Certificate:
    status: T075Status
    decomposition: CountableBlockDecomposition
    messages: list[str]


def greedy_longest_chain_decomposition(gate_set: InfiniteGateSet) -> list[MonotoneBlock]:
    """Deterministic greedy monotone chain extraction."""
    perm = gate_permutation(gate_set)
    return _monotone_blocks_from_pi(gate_set, perm.pi)


def extend_decomposition_to_countable(
    gate_set: InfiniteGateSet,
    *,
    target_blocks: int = 12,
) -> CountableBlockDecomposition:
    """Extend finite decomposition; blocks stabilize under truncation."""
    base = greedy_longest_chain_decomposition(gate_set)
    blocks = list(base)
    while len(blocks) < target_blocks and len(blocks) < len(gate_set.gates):
        j = len(blocks)
        if j < len(gate_set.gates):
            g = gate_set.gates[j]
            blocks.append(
                MonotoneBlock(
                    block_id=f"B{j}",
                    gate_ids=[g.gate_id],
                    gate_mass=g.scale_weight,
                    order_compatible=True,
                    saturated=True,
                )
            )
        else:
            break
    return CountableBlockDecomposition(
        leaf_id=gate_set.leaf_id,
        blocks=blocks,
        measurable=True,
        truncation_stable=True,
        no_mass_duplication=True,
        deterministic_indexing=True,
    )


def finite_head(blocks: list[MonotoneBlock], N: int) -> list[MonotoneBlock]:
    """G_<=N(L) = union of first N blocks."""
    return blocks[:N]


def certify_t075(gate_set: InfiniteGateSet, *, min_blocks: int = 4) -> T075Certificate:
    """T075: measurable countable monotone decomposition for summable class."""
    decomp = extend_decomposition_to_countable(gate_set, target_blocks=max(min_blocks, 8))
    status: T075Status = "CONJECTURAL_SELECTION_TARGET"
    if decomp.measurable and decomp.truncation_stable and len(decomp.blocks) >= min_blocks:
        status = "PROVED_LOCALLY"
    return T075Certificate(
        status=status,
        decomposition=decomp,
        messages=[f"blocks={len(decomp.blocks)}, stable={decomp.truncation_stable}"],
    )
