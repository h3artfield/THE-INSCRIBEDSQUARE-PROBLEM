"""Gate-tail attachment signature (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.gate_tail_defect import GateTailDefect, defect_tail_N
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.saturated_gate_truncation import SaturatedTruncation


@dataclass
class GateTailSignature:
    leaf_id: str
    level: int
    sig_tail: float
    cross_interaction: float
    exceeds_intrinsic_only: bool


def sig_tail_N(sat: SaturatedTruncation, gate_set: InfiniteGateSet) -> GateTailSignature:
    """SigTail_N = sup attachment area from omitted gates + retained interactions."""
    defect = defect_tail_N(sat, gate_set)
    cross = defect.gate_interaction + defect.join_terms
    sig = defect.total_defect
    intrinsic_only = defect.intrinsic_ear_area
    return GateTailSignature(
        leaf_id=sat.leaf_id,
        level=sat.level,
        sig_tail=sig,
        cross_interaction=cross,
        exceeds_intrinsic_only=sig > intrinsic_only * 1.5,
    )


def tail_signature_tends_zero(signatures: list[GateTailSignature]) -> bool:
    if len(signatures) < 2:
        return signatures[0].sig_tail < 0.05 if signatures else False
    return signatures[-1].sig_tail <= signatures[0].sig_tail and signatures[-1].sig_tail < 0.08
