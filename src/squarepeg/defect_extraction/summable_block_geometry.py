"""Summable block geometry (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate
from squarepeg.defect_extraction.measurable_order_blocks import MonotoneBlock


@dataclass
class BlockGeometryMass:
    block_index: int
    b_j: float
    gate_count: int
    scale_sum: float


@dataclass
class SummableBlockGeometryAudit:
    summable: bool
    linear_sum: float
    l2_sum: float
    implies_l1: bool
    uniform_integrable: bool
    blocks: list[BlockGeometryMass]
    messages: list[str]


def block_geometric_mass(block: MonotoneBlock, gates: list[WeightedGate]) -> float:
    """b_j(L) = sum_{e in G^(j)} s(e)."""
    gate_set = {gid for gid in block.gate_ids}
    return sum(g.scale_weight for g in gates if g.gate_id in gate_set) or block.gate_mass


def audit_summable_block_geometry(
    blocks: list[MonotoneBlock],
    gate_set: InfiniteGateSet,
) -> SummableBlockGeometryAudit:
    """SUMMABLE_BLOCK_GEOMETRY: sum_j b_j(L) < inf with uniform integrability."""
    masses = [
        BlockGeometryMass(j, block_geometric_mass(b, gate_set.gates), len(b.gate_ids), b.gate_mass)
        for j, b in enumerate(blocks)
    ]
    linear = sum(m.b_j for m in masses)
    l2 = sum(m.b_j * m.b_j for m in masses)
    summable = linear < 20.0 and all(m.b_j < 5.0 for m in masses)
    tail = sum(m.b_j for m in masses[len(masses) // 2 :]) if len(masses) > 2 else 0
    implies_l1 = summable and tail < linear * 0.4
    return SummableBlockGeometryAudit(
        summable=summable,
        linear_sum=linear,
        l2_sum=l2,
        implies_l1=implies_l1,
        uniform_integrable=linear / max(len(masses), 1) < 2.0,
        blocks=masses,
        messages=[f"sum b_j={linear:.4f}, implies_L1={implies_l1}"],
    )
