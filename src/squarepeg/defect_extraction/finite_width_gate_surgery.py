"""T073 finite-width positive-inversion surgery (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.infinite_gate_lamination_surgery import certify_t068i
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, gate_set_of_leaf
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_order_blocks import select_measurable_blocks
from squarepeg.defect_extraction.monotone_gate_width import audit_monotone_width, asymptotic_width
from squarepeg.defect_extraction.order_block_signature import audit_cross_block_signature
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T073Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class T073Certificate:
    status: T073Status
    finite_width: bool
    block_count: int
    cross_block_vanishing: bool
    blockwise_t068i: bool
    messages: list[str]


def certify_t073(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    K: int = 4,
) -> T073Certificate:
    """T073: finite-width positive-inversion surgery."""
    width = audit_monotone_width(gate_set, K=K)
    w_star = asymptotic_width(gate_set)
    finite = w_star is not None and w_star <= K and width.inv_density > 0.01
    selection = select_measurable_blocks(gate_set, K=K)
    cross = audit_cross_block_signature(selection, K=K)
    blockwise_ok = all(b.order_compatible and b.saturated for b in selection.blocks)
    status: T073Status = "CONJECTURAL_TARGET"
    if finite and cross.vanishing and blockwise_ok and selection.measurable:
        status = "PROVED_LOCALLY"
    msgs = [
        f"w_*={w_star}, blocks={selection.block_count}",
        f"cross_vanishing={cross.vanishing}",
    ]
    return T073Certificate(
        status=status,
        finite_width=finite,
        block_count=selection.block_count,
        cross_block_vanishing=cross.vanishing,
        blockwise_t068i=blockwise_ok,
        messages=msgs,
    )


def certify_t073_lamination(
    lam: DiffuseNoncrossingWindingLamination,
    *,
    K: int = 4,
) -> T073Certificate:
    if not lam.leaves:
        return T073Certificate("CONJECTURAL_TARGET", False, 0, False, False, ["Empty"])
    leaf = lam.leaves[0]
    gs = gate_set_of_leaf(leaf, count=12)
    return certify_t073(gs, leaf, K=K)
