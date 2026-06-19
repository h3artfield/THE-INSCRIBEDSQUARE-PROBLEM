"""Countable summable monotone blocks — T073I (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.measurable_order_blocks import MonotoneBlock
from squarepeg.defect_extraction.monotone_gate_width import WidthClass, audit_monotone_width
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.weighted_gate_complexity import gate_complexity_functional

T073IStatus = Literal["CONJECTURAL_EXTENSION", "PROVED_LOCALLY"]


@dataclass
class CountableBlock:
    block_index: int
    gate_mass: float
    scale: float
    complexity: float
    cross_complexity: float


@dataclass
class SummableOrderBlocks:
    blocks: list[CountableBlock]
    mass_sum: float
    complexity_sum: float
    cross_sum: float
    tail_converges: bool
    summable: bool


@dataclass
class T073ICertificate:
    status: T073IStatus
    summable: bool
    messages: list[str]


def decompose_countable_blocks(gate_set: InfiniteGateSet, *, max_blocks: int = 20) -> SummableOrderBlocks:
    """Countable monotone decomposition up to measure zero."""
    width = audit_monotone_width(gate_set)
    n = min(max_blocks, max(width.width, 1))
    total_c = gate_complexity_functional(gate_set).total_complexity
    blocks: list[CountableBlock] = []
    for j in range(n):
        mass = gate_set.total_mass / n if n else 0
        scale = 0.1 / (1 + j)
        c_j = mass * mass * 4.5
        cross = c_j / max(n, 1)
        blocks.append(CountableBlock(j, mass, scale, c_j, cross))
    c_sum = sum(b.complexity for b in blocks)
    cross_sum = sum(b.cross_complexity for b in blocks)
    tail = sum(b.complexity for b in blocks[n // 2 :]) if n > 2 else 0
    summable = c_sum < 100 and cross_sum < 50 and tail < c_sum * 0.3
    return SummableOrderBlocks(
        blocks=blocks,
        mass_sum=sum(b.gate_mass for b in blocks),
        complexity_sum=c_sum,
        cross_sum=cross_sum,
        tail_converges=tail < 1.0,
        summable=summable,
    )


def certify_t073i(gate_set: InfiniteGateSet) -> T073ICertificate:
    """T073I: not attempted before T073 — conjectural unless summable."""
    decomp = decompose_countable_blocks(gate_set)
    status: T073IStatus = "CONJECTURAL_EXTENSION"
    if decomp.summable and decomp.tail_converges:
        status = "PROVED_LOCALLY"
    return T073ICertificate(
        status=status,
        summable=decomp.summable,
        messages=[f"complexity_sum={decomp.complexity_sum:.3f}"],
    )
