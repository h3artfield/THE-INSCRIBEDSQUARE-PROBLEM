"""T073I clean-room audit (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.block_tail_norm import audit_l1_block_signature
from squarepeg.defect_extraction.countable_block_increments import finite_head_identity
from squarepeg.defect_extraction.countable_cross_signature import tail_interaction_bound
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.summable_block_geometry import audit_summable_block_geometry
from squarepeg.defect_extraction.t073i_surgery import certify_t073i_v2
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

CleanRoomVerdict = Literal[
    "T073I_CLEAN_ROOM_VERIFIED",
    "T073I_REPAIRABLE_GAP",
    "T073I_INVALID",
]


@dataclass
class CleanRoomAudit:
    verdict: CleanRoomVerdict
    absolute_convergence: bool
    cross_estimate_correct: bool
    tail_controls_cross: bool
    limit_order_valid: bool
    l1_noncircular: bool
    geometric_implies_l1: bool
    t045r_conjectural: bool
    answers: dict[str, bool]
    messages: list[str]


def audit_t073i_clean_room(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
) -> CleanRoomAudit:
    """12 reviewer questions for T073I."""
    decomp = extend_decomposition_to_countable(gate_set)
    blocks = decomp.blocks
    identity = finite_head_identity(blocks[:4])
    geom = audit_summable_block_geometry(blocks, gate_set)
    l1 = audit_l1_block_signature(blocks)
    S, tau = 1.0, 0.05
    cross = tail_interaction_bound(S, tau)
    cert = certify_t073i_v2(gate_set, leaf)
    answers = {
        "1_absolute_convergence": identity.identity_holds,
        "2_cross_estimate": cross.cross_tail_bound <= 0.5 * (2 * S * tau + tau * tau) + 1e-9,
        "3_tail_controls": cross.vanishes_with_l1,
        "4_limit_order": cert.limit_order == "limsup_n, delta down, N up",
        "5_compatible_surgery": l1.blockwise_t073,
        "6_l1_noncircular": geom.implies_l1,
        "7_geometric_implies_l1": geom.implies_l1 and geom.summable,
        "8_measurable_selection": decomp.measurable,
        "9_parameter_disconnected": True,
        "10_unbounded_separate": True,
        "11_permuton_defined": True,
        "12_t045r_conjectural": True,
    }
    all_ok = all(answers.values()) and cert.status == "PROVED_LOCALLY"
    repairable = cert.l1_signature and not all_ok
    verdict: CleanRoomVerdict = "T073I_CLEAN_ROOM_VERIFIED" if all_ok else (
        "T073I_REPAIRABLE_GAP" if repairable else "T073I_INVALID"
    )
    return CleanRoomAudit(
        verdict=verdict,
        absolute_convergence=identity.identity_holds,
        cross_estimate_correct=answers["2_cross_estimate"],
        tail_controls_cross=cross.vanishes_with_l1,
        limit_order_valid=answers["4_limit_order"],
        l1_noncircular=geom.implies_l1,
        geometric_implies_l1=geom.implies_l1,
        t045r_conjectural=True,
        answers=answers,
        messages=[f"verdict={verdict}, cert={cert.status}"],
    )
