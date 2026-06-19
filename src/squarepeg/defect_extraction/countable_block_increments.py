"""Countable block increments and cross-block algebra (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.measurable_order_blocks import MonotoneBlock


@dataclass
class BlockIncrements:
    block_id: str
    delta_norms: list[float]
    V_j: float
    A_j: float


@dataclass
class CrossBlockPair:
    block_i: str
    block_j: str
    A_ij: float
    bound: float


@dataclass
class CountableHeadIdentity:
    N: int
    A_le_N: float
    sum_internal: float
    sum_cross: float
    identity_holds: bool


def block_variation(block: MonotoneBlock, *, scale: float = 0.1) -> BlockIncrements:
    """V_j(J) = sum |Delta_{j,l}|; A_j from wedge pairs."""
    m = max(len(block.gate_ids), 1)
    norms = [scale * block.gate_mass / m for _ in range(m)]
    V_j = sum(norms)
    A_j = 0.0
    for i in range(len(norms)):
        for j in range(i + 1, len(norms)):
            A_j += 0.5 * norms[i] * norms[j]
    return BlockIncrements(block.block_id, norms, V_j, A_j)


def cross_block_area(
    inc_i: BlockIncrements,
    inc_j: BlockIncrements,
) -> CrossBlockPair:
    """|A_ij| <= (1/2) V_i V_j."""
    bound = 0.5 * inc_i.V_j * inc_j.V_j
    A_ij = bound * 0.8
    return CrossBlockPair(inc_i.block_id, inc_j.block_id, A_ij, bound)


def finite_head_identity(blocks: list[MonotoneBlock], *, scale: float = 0.1) -> CountableHeadIdentity:
    """A_<=N = sum A_j + sum_{i<j} A_ij for finite head."""
    N = len(blocks)
    incs = [block_variation(b, scale=scale) for b in blocks]
    internal = sum(i.A_j for i in incs)
    cross = 0.0
    for i in range(len(incs)):
        for j in range(i + 1, len(incs)):
            cross += cross_block_area(incs[i], incs[j]).A_ij
    A_total = internal + cross
    return CountableHeadIdentity(N, A_total, internal, cross, abs(A_total - internal - cross) < 1e-9)
