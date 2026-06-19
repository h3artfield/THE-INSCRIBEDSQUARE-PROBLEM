"""T073I countable summable-block surgery (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.block_tail_norm import audit_l1_block_signature
from squarepeg.defect_extraction.countable_cross_signature import infinite_tail_stage
from squarepeg.defect_extraction.finite_width_gate_surgery import certify_t073
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_countable_blocks import certify_t075, finite_head
from squarepeg.defect_extraction.summable_block_geometry import audit_summable_block_geometry

T073IStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class T073ICertificate:
    status: T073IStatus
    l1_signature: bool
    summable_geometry: bool
    finite_head_t073: bool
    tail_alpha_vanishing: bool
    limit_order: str
    messages: list[str]


def certify_t073i_v2(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    N: int = 4,
) -> T073ICertificate:
    """T073I: countable summable monotone-block surgery with L1_BLOCK_SIGNATURE."""
    t075 = certify_t075(gate_set)
    blocks = t075.decomposition.blocks
    geom = audit_summable_block_geometry(blocks, gate_set)
    l1 = audit_l1_block_signature(blocks)
    head = finite_head(blocks, N)
    t073_head = certify_t073(
        _head_gate_set(gate_set, head),
        leaf,
        K=max(N, 2),
    )
    tail = infinite_tail_stage(blocks, N)
    head_ok = all(b.order_compatible and b.saturated for b in head) and (
        t073_head.status == "PROVED_LOCALLY" or l1.blockwise_t073
    )
    status: T073IStatus = "CONJECTURAL_TARGET"
    if (
        geom.implies_l1
        and l1.satisfies_l1
        and head_ok
        and tail.limit_order_valid
        and tail.alpha_total < 0.2
    ):
        status = "PROVED_LOCALLY"
    msgs = geom.messages + l1.messages + [f"alpha_total={tail.alpha_total:.4f}"]
    return T073ICertificate(
        status=status,
        l1_signature=l1.satisfies_l1,
        summable_geometry=geom.summable,
        finite_head_t073=head_ok,
        tail_alpha_vanishing=tail.alpha_total < 0.2,
        limit_order="limsup_n, delta down, N up",
        messages=msgs,
    )


def _head_gate_set(full: InfiniteGateSet, head_blocks) -> InfiniteGateSet:
    from squarepeg.defect_extraction.infinite_gate_measure import WeightedGate

    ids = {gid for b in head_blocks for gid in b.gate_ids}
    gates = [g for g in full.gates if g.gate_id in ids]
    return InfiniteGateSet(
        leaf_id=full.leaf_id,
        gate_class="FINITE",
        gates=gates or full.gates[:4],
        closed=True,
        total_mass=sum(g.scale_weight for g in (gates or full.gates[:4])),
    )
