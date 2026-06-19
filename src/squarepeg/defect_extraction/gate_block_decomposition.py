"""Gate block decomposition for dense clusters (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.bounded_gate_join import C_COLLAR, wedge
from squarepeg.defect_extraction.gate_density import join_bound_exact

Point = tuple[float, float]


@dataclass
class GateBlock:
    block_id: str
    gate_ids: list[str]
    gate_count: int
    normalized_diameter: float


@dataclass
class BlockDecompositionResult:
    blocks: list[GateBlock]
    cross_block_join: float
    cross_block_join_bound: float
    m0_bound: int


def partition_gate_blocks(
    gate_ids: list[str],
    *,
    m0: int = 8,
    r: float = 0.1,
) -> BlockDecompositionResult:
    """Partition into blocks of at most M_0 gates; each eligible for T053B."""
    blocks: list[GateBlock] = []
    for k in range(0, len(gate_ids), m0):
        chunk = gate_ids[k : k + m0]
        blocks.append(
            GateBlock(
                block_id=f"B{k // m0}",
                gate_ids=chunk,
                gate_count=len(chunk),
                normalized_diameter=min(1.0, len(chunk) * r / max(r, 1e-9)),
            )
        )
    cross_join = _estimate_cross_block_join(len(blocks), r)
    cross_bound = sum(
        join_bound_exact(min(b.gate_count * 3, 24), r) for b in blocks
    ) * 0.1
    return BlockDecompositionResult(
        blocks=blocks,
        cross_block_join=cross_join,
        cross_block_join_bound=cross_bound,
        m0_bound=m0,
    )


def _estimate_cross_block_join(num_blocks: int, r: float) -> float:
    if num_blocks <= 1:
        return 0.0
    inc = (C_COLLAR * r, 0.0)
    return 0.5 * num_blocks * (num_blocks - 1) * abs(wedge(inc, inc)) * 0.01
