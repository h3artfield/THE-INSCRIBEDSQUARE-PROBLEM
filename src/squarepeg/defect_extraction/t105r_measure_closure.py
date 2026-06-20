"""T105R — Gate-order-augmented measure transition closure (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_measure_tightness import audit_gate_measure_tightness
from squarepeg.defect_extraction.gate_measure_weak_closure import certify_t107
from squarepeg.defect_extraction.gate_order_realizability import audit_gate_order_realizability

T105RStatus = Literal["CONJECTURAL_MEASURE_CLOSURE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T105RCertificate:
    status: T105RStatus
    sequentially_compact: bool
    recursion_closed: bool
    supersedes_t105: bool
    messages: list[str]


def certify_t105r(tree: CanonicalIntrusionTree) -> T105RCertificate:
    t107 = certify_t107(tree)
    tight = audit_gate_measure_tightness(tree)
    real = audit_gate_order_realizability(tree)
    closed = (
        t107.status == "PROVED_LOCALLY"
        and t107.sequentially_closed
        and tight.all_tight
        and real.all_realizable
    )
    status: T105RStatus = "PROVED_LOCALLY" if closed else "CONJECTURAL_MEASURE_CLOSURE_TARGET"
    return T105RCertificate(status, closed, closed, closed, [f"t107={t107.status}, closed={closed}"])
