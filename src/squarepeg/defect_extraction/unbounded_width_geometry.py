"""Unbounded order width geometry — T074R (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, longest_decreasing_subsequence
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.noncrossing_order_width import audit_forbidden_patterns, certify_t074

T074RStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T074ROutcome = Literal[
    "INFINITE_INTRUSION_TREE",
    "UNBOUNDED_BRANCHING",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "DIFFUSE_PERMUTON",
    "FINITE_OR_COUNTABLE_SURGERY",
]


@dataclass
class T074RCertificate:
    status: T074RStatus
    outcome: T074ROutcome
    width_unbounded: bool
    lds_length: int
    pattern_class: str
    messages: list[str]


def certify_t074r(gate_set: InfiniteGateSet, *, K: int = 4) -> T074RCertificate:
    """T074R: unbounded width geometric reduction."""
    t074 = certify_t074(gate_set, K=K)
    perm = gate_permutation(gate_set)
    lds = longest_decreasing_subsequence(perm.pi)
    pattern = audit_forbidden_patterns(perm.pi)
    unbounded = lds > K + 1
    outcome: T074ROutcome = "FINITE_OR_COUNTABLE_SURGERY"
    if unbounded:
        if t074.outcome == "INFINITE_INTRUSION_RAY":
            outcome = "INFINITE_INTRUSION_TREE"
        elif t074.outcome == "UNBOUNDED_BRANCHING":
            outcome = "UNBOUNDED_BRANCHING"
        elif pattern == "BROADER_PATTERN_CLASS":
            outcome = "DIFFUSE_PERMUTON"
        else:
            outcome = "PARAMETER_DISCONNECTED"
    return T074RCertificate(
        status="PROVED_LOCALLY_CLASSIFIER",
        outcome=outcome,
        width_unbounded=unbounded,
        lds_length=lds,
        pattern_class=pattern,
        messages=[f"lds={lds}, outcome={outcome}"],
    )
