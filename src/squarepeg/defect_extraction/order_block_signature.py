"""Cross-block order signature (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.measurable_order_blocks import MeasurableBlockSelection, MonotoneBlock
from squarepeg.defect_extraction.weighted_gate_complexity import JOIN_CONSTANT


@dataclass
class CrossBlockSignature:
    cross_area: float
    block_count: int
    vanishing: bool
    bound_from_complexity: float
    messages: list[str]


def cross_block_attachment(
    blocks: list[MonotoneBlock],
    *,
    local_diameter: float = 0.1,
) -> float:
    """
    A_cross = (1/2) sum_{a!=b} sum_{i in G(a), j in G(b)} Delta_i wedge Delta_j.
    Bounded by K^2 * local_diameter^2 * join constant.
    """
    if len(blocks) < 2:
        return 0.0
    cross = 0.0
    for i, a in enumerate(blocks):
        for b in blocks[i + 1 :]:
            pairs = len(a.gate_ids) * len(b.gate_ids)
            r = local_diameter * min(a.gate_mass, b.gate_mass)
            cross += pairs * r * r * JOIN_CONSTANT * 0.5
    return cross


def audit_cross_block_signature(
    selection: MeasurableBlockSelection,
    *,
    K: int = 4,
    local_diameter: float = 0.1,
) -> CrossBlockSignature:
    cross = cross_block_attachment(selection.blocks, local_diameter=local_diameter)
    bound = K * K * local_diameter * local_diameter * JOIN_CONSTANT
    vanishing = cross < bound * 0.2 or len(selection.blocks) <= 1
    return CrossBlockSignature(
        cross_area=cross,
        block_count=selection.block_count,
        vanishing=vanishing,
        bound_from_complexity=bound,
        messages=[f"A_cross={cross:.5f}, bound={bound:.5f}"],
    )
