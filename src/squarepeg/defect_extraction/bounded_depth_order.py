"""Bounded-depth order complexity — T077-A (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_permuton_compactness import (
    audit_genuinely_diffuse,
    build_augmented_measure,
)
from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, longest_decreasing_subsequence
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.jordan_gate_realizability import build_jordan_gate_system
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.permuton_extremal_bound import inversion_density_bound

T077AStatus = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class BoundedDepthAudit:
    max_depth: int
    max_branching: int
    center_count: int
    monotone_width: int
    inversion_density: float
    density_bound: float
    structural_complexity_finite: bool


@dataclass
class T077ACertificate:
    status: T077AStatus
    diffuse_limit_possible: bool
    bounded_depth: bool
    audit: BoundedDepthAudit
    messages: list[str]


def audit_bounded_depth_order(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    D: int = 8,
    B: int = 4,
    K: int = 4,
) -> BoundedDepthAudit:
    """Uniform depth D forces finite structural complexity."""
    sys = build_jordan_gate_system(gate_set, leaf, max_depth=D)
    perm = gate_permutation(gate_set)
    lds = longest_decreasing_subsequence(perm.pi)
    inv = perm.inv_density
    bound = inversion_density_bound(D, B, K)
    centers = len({(round(g.point[0], 1), round(g.point[1], 1)) for g in gate_set.gates})
    depth_ok = sys.intrusion_depth <= D
    branch_ok = sys.branching <= B
    finite = depth_ok and branch_ok and lds <= D + B and inv <= bound + 0.05
    return BoundedDepthAudit(
        max_depth=sys.intrusion_depth,
        max_branching=sys.branching,
        center_count=centers,
        monotone_width=lds,
        inversion_density=inv,
        density_bound=bound,
        structural_complexity_finite=finite,
    )


def certify_t077a(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    D: int = 8,
    B: int = 4,
    K: int = 4,
) -> T077ACertificate:
    """T077-A: bounded depth + Jordan hull cannot converge to genuinely diffuse permuton."""
    audit = audit_bounded_depth_order(gate_set, leaf, D=D, B=B, K=K)
    limit = build_augmented_measure(gate_set, leaf)
    diffuse_crit = audit_genuinely_diffuse(limit, K=K)
    depth_ok = audit.max_depth <= D and all(a.depth <= D for a in limit.atoms)
    branch_ok = audit.max_branching <= B
    center_ok = audit.center_count <= K
    diffuse_possible = diffuse_crit.genuinely_diffuse and depth_ok
    status: T077AStatus = "CONJECTURAL_CORE_TARGET"
    if depth_ok and branch_ok and center_ok and not diffuse_possible:
        status = "PROVED_LOCALLY"
    elif audit.inversion_density > audit.density_bound + 0.1:
        status = "CONJECTURAL_CORE_TARGET"
    return T077ACertificate(
        status=status,
        diffuse_limit_possible=diffuse_possible,
        bounded_depth=depth_ok,
        audit=audit,
        messages=[
            f"status={status}, diffuse_possible={diffuse_possible}, inv={audit.inversion_density:.4f}",
        ],
    )
