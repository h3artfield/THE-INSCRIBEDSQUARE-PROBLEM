"""Intrusion depth from decreasing orders — T074R (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, longest_decreasing_subsequence
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.realizable_gate_permutations import audit_realizable_permutation
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

T074RStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T074ROutcome = Literal[
    "INFINITE_NESTED_RAY",
    "UNBOUNDED_BRANCHING",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_LIMIT",
    "MULTICENTER_PROLIFERATION",
    "FINITE_OR_COUNTABLE_SURGERY",
    "DIFFUSE_REALIZABLE_PERMUTON",
]


@dataclass
class DecreasingSubsequenceGeometry:
    length: int
    nested: bool
    branching_estimate: int
    forces_intrusion_ray: bool


@dataclass
class T074RCertificate:
    status: T074RStatus
    outcome: T074ROutcome
    lds_length: int
    nested_arcs: bool
    messages: list[str]


def decreasing_subsequence_geometry(gate_set: InfiniteGateSet) -> DecreasingSubsequenceGeometry:
    perm = gate_permutation(gate_set)
    lds = longest_decreasing_subsequence(perm.pi)
    nested = lds >= 3 and perm.inv_density > 0.05
    branching = max(0, lds - 2)
    ray = lds >= 6 and nested
    return DecreasingSubsequenceGeometry(lds, nested, branching, ray)


def certify_t074r_v2(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    K: int = 4,
) -> T074RCertificate:
    """T074R using planar topology from realizable permutations."""
    real = audit_realizable_permutation(gate_set, leaf)
    geom = decreasing_subsequence_geometry(gate_set)
    outcome: T074ROutcome = "FINITE_OR_COUNTABLE_SURGERY"
    status: T074RStatus = "CONJECTURAL_STRUCTURAL_TARGET"
    if not real.realizable:
        outcome = "NON_JORDAN_LIMIT"
    elif geom.forces_intrusion_ray:
        outcome = "INFINITE_NESTED_RAY"
        status = "PROVED_LOCALLY_PARTIAL"
    elif geom.branching_estimate > K:
        outcome = "UNBOUNDED_BRANCHING"
        status = "PROVED_LOCALLY_PARTIAL"
    elif geom.length > K + 2:
        outcome = "MULTICENTER_PROLIFERATION"
    elif geom.length <= K:
        outcome = "FINITE_OR_COUNTABLE_SURGERY"
        status = "PROVED_LOCALLY_PARTIAL"
    return T074RCertificate(
        status=status,
        outcome=outcome,
        lds_length=geom.length,
        nested_arcs=geom.nested,
        messages=[f"LDS={geom.length}, nested={geom.nested}"],
    )
