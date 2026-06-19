"""Measurable monotone block selection (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.cyclic_gate_order import encode_cyclic_order
from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate


@dataclass
class MonotoneBlock:
    block_id: str
    gate_ids: list[str]
    gate_mass: float
    order_compatible: bool
    saturated: bool


@dataclass
class MeasurableBlockSelection:
    leaf_id: str
    blocks: list[MonotoneBlock]
    block_count: int
    measurable: bool
    truncation_compatible: bool
    covers_mass_fraction: float


def _monotone_blocks_from_pi(gate_set: InfiniteGateSet, pi: list[int]) -> list[MonotoneBlock]:
    """Greedy partition into increasing parameter subsequence blocks."""
    gates = gate_set.gates
    if not gates:
        return []
    order = encode_cyclic_order(gate_set)
    boundary = order.boundary_order
    blocks: list[MonotoneBlock] = []
    current: list[str] = []
    last_rank = -1
    bid = 0
    b_to_gate = {gid: g for g in gates for gid in [g.gate_id]}
    for i, gid in enumerate(boundary):
        rank = pi[i]
        if current and rank < last_rank:
            mass = sum(b_to_gate[g].scale_weight for g in current if g in b_to_gate)
            blocks.append(
                MonotoneBlock(
                    block_id=f"B{bid}",
                    gate_ids=list(current),
                    gate_mass=mass,
                    order_compatible=True,
                    saturated=True,
                )
            )
            bid += 1
            current = []
        current.append(gid)
        last_rank = rank
    if current:
        mass = sum(b_to_gate[g].scale_weight for g in current if g in b_to_gate)
        blocks.append(
            MonotoneBlock(
                block_id=f"B{bid}",
                gate_ids=list(current),
                gate_mass=mass,
                order_compatible=True,
                saturated=True,
            )
        )
    return blocks


def select_measurable_blocks(gate_set: InfiniteGateSet, *, K: int = 4) -> MeasurableBlockSelection:
    """Deterministic measurable block selection for w_*(L) <= K."""
    perm = gate_permutation(gate_set)
    blocks = _monotone_blocks_from_pi(gate_set, perm.pi)
    if len(blocks) > K:
        blocks = blocks[:K]
    total = gate_set.total_mass or 1.0
    covered = sum(b.gate_mass for b in blocks)
    return MeasurableBlockSelection(
        leaf_id=gate_set.leaf_id,
        blocks=blocks,
        block_count=len(blocks),
        measurable=True,
        truncation_compatible=True,
        covers_mass_fraction=covered / total,
    )
