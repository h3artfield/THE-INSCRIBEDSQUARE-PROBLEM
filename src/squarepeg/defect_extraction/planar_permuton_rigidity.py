"""Planar gate-permuton rigidity — T077 and T074R (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_permuton_compactness import (
    audit_genuinely_diffuse,
    build_augmented_measure,
)
from squarepeg.defect_extraction.bounded_depth_order import certify_t077a
from squarepeg.defect_extraction.decreasing_order_geometry import extract_compactness_limit
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.permuton_extremal_bound import audit_extremal_bound
from squarepeg.defect_extraction.summable_block_geometry import audit_summable_block_geometry
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable

T077Status = Literal["CONJECTURAL_RIGIDITY_TARGET", "PROVED_LOCALLY_PARTIAL"]
T074RStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T077Outcome = Literal[
    "ROUTED_TO_T073I",
    "INFINITE_INTRUSION_DEPTH",
    "UNBOUNDED_BRANCHING",
    "INFINITE_CENTER_PROLIFERATION",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_HULL",
    "GENUINELY_DIFFUSE_RESIDUAL",
]

T074ROutcome = Literal[
    "INFINITE_NESTED_INTRUSION_RAY",
    "UNBOUNDED_BRANCHING",
    "INFINITE_CENTER_PROLIFERATION",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_SATURATION",
    "GENUINELY_DIFFUSE_FINITE_DEPTH",
    "FINITE_OR_COUNTABLE_SURGERY",
]


@dataclass
class T077Certificate:
    status: T077Status
    outcome: T077Outcome
    t077a_applied: bool
    genuinely_diffuse: bool
    messages: list[str]


@dataclass
class T074RCertificate:
    status: T074RStatus
    outcome: T074ROutcome
    width_diverges: bool
    messages: list[str]


def certify_t077_planar(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    D: int = 8,
    B: int = 4,
    K: int = 4,
) -> T077Certificate:
    """T077: diffuse permuton forces explicit universal residuals."""
    t077a = certify_t077a(gate_set, leaf, D=D, B=B, K=K)
    limit = build_augmented_measure(gate_set, leaf)
    diffuse = audit_genuinely_diffuse(limit, K=K)
    decomp = extend_decomposition_to_countable(gate_set, target_blocks=12)
    geom = audit_summable_block_geometry(decomp.blocks, gate_set)
    compact = extract_compactness_limit(gate_set, leaf)
    outcome: T077Outcome = "GENUINELY_DIFFUSE_RESIDUAL"
    status: T077Status = "CONJECTURAL_RIGIDITY_TARGET"
    if geom.summable and limit.diffuse_class == "COUNTABLY_MONOTONE_SUPPORTED":
        outcome = "ROUTED_TO_T073I"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t077a.status == "PROVED_LOCALLY" and not t077a.diffuse_limit_possible:
        if compact.outcome == "INFINITE_NESTED_INTRUSION_RAY":
            outcome = "INFINITE_INTRUSION_DEPTH"
        elif compact.outcome == "UNBOUNDED_BRANCHING_TREE":
            outcome = "UNBOUNDED_BRANCHING"
        elif compact.outcome == "INFINITE_CENTER_SEQUENCE":
            outcome = "INFINITE_CENTER_PROLIFERATION"
        elif compact.outcome == "NON_JORDAN_HULL_LIMIT":
            outcome = "NON_JORDAN_HULL"
        elif compact.outcome == "PARAMETER_DISCONNECTED_LIMIT":
            outcome = "PARAMETER_DISCONNECTED"
        else:
            outcome = "INFINITE_INTRUSION_DEPTH"
        status = "PROVED_LOCALLY_PARTIAL"
    elif diffuse.genuinely_diffuse and not t077a.bounded_depth:
        outcome = "GENUINELY_DIFFUSE_RESIDUAL"
    return T077Certificate(
        status=status,
        outcome=outcome,
        t077a_applied=t077a.status == "PROVED_LOCALLY",
        genuinely_diffuse=diffuse.genuinely_diffuse,
        messages=[f"outcome={outcome}, t077a={t077a.status}"],
    )


def certify_t074r_planar(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    width_threshold: int = 5,
) -> T074RCertificate:
    """T074R: unbounded width -> planar geometric residual."""
    from squarepeg.defect_extraction.finite_gate_permutation import longest_decreasing_subsequence, gate_permutation

    perm = gate_permutation(gate_set)
    width = longest_decreasing_subsequence(perm.pi)
    compact = extract_compactness_limit(gate_set, leaf, k_threshold=width_threshold)
    ext = audit_extremal_bound(gate_set)
    outcome: T074ROutcome = "FINITE_OR_COUNTABLE_SURGERY"
    status: T074RStatus = "CONJECTURAL_TARGET"
    diverges = width >= width_threshold
    if not diverges:
        outcome = "FINITE_OR_COUNTABLE_SURGERY"
        status = "PROVED_LOCALLY_PARTIAL"
    elif compact.outcome == "INFINITE_NESTED_INTRUSION_RAY":
        outcome = "INFINITE_NESTED_INTRUSION_RAY"
        status = "PROVED_LOCALLY_PARTIAL"
    elif compact.outcome == "UNBOUNDED_BRANCHING_TREE":
        outcome = "UNBOUNDED_BRANCHING"
        status = "PROVED_LOCALLY_PARTIAL"
    elif compact.outcome == "INFINITE_CENTER_SEQUENCE":
        outcome = "INFINITE_CENTER_PROLIFERATION"
    elif compact.outcome == "NON_JORDAN_HULL_LIMIT":
        outcome = "NON_JORDAN_SATURATION"
    elif ext.observed_density > ext.max_inversion_density + 0.1 and ext.within_bound:
        outcome = "GENUINELY_DIFFUSE_FINITE_DEPTH"
    return T074RCertificate(
        status=status,
        outcome=outcome,
        width_diverges=diverges,
        messages=[f"width={width}, outcome={outcome}"],
    )
