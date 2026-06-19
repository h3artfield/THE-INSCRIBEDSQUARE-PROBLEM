"""Intrinsic tree nonsummability quantities (Directive 043)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.countable_child_identity import L_v, tau_v
from squarepeg.defect_extraction.countable_child_order import extract_countable_family
from squarepeg.defect_extraction.finite_subtree_exhaustion import audit_exhaustion
from squarepeg.defect_extraction.intrusion_ray_geometry import extract_ray
from squarepeg.defect_extraction.summable_ray_signature import build_attachment_chains, ray_scale_mass
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure

TreeFailureClass = Literal[
    "CHILD_LINEAR_NONSUMMABILITY",
    "CHILD_CROSS_SIGNATURE_NONSUMMABILITY",
    "RAY_SIGNATURE_NONSUMMABILITY",
    "DIFFUSE_END_NONSUMMABILITY",
    "MULTIPLE_TREE_FAILURES",
    "NONE",
]

SummabilityStatus = Literal["SUMMABLE", "NONSUMMABLE", "MIXED"]


@dataclass
class ChildNonsummabilityRecord:
    node_id: str
    N_child: float
    L_v: float
    linear_nonsummable: bool
    cross_nonsummable: bool


@dataclass
class RayNonsummabilityRecord:
    S_ray: float
    tail_cost: float
    N_ray: float
    nonsummable: bool


@dataclass
class TreeNonsummabilityRecord:
    N_tree: float
    intrinsic_tail: float
    nonsummable: bool


@dataclass
class IntrinsicTreeNonsummabilityAudit:
    child_records: list[ChildNonsummabilityRecord]
    ray_record: RayNonsummabilityRecord | None
    tree_record: TreeNonsummabilityRecord
    failure_class: TreeFailureClass
    summability: SummabilityStatus
    messages: list[str]


def N_child(v_records_len: int, tail_fn, *, eta_0: float = 0.02) -> float:
    """inf over compatible exhaustions liminf tau_v(N); geometric order proxy."""
    if v_records_len == 0:
        return 0.0
    tails = [tail_fn(N) for N in range(1, min(v_records_len, 20))]
    if not tails:
        return 0.0
    return min(tails[-3:]) if len(tails) >= 3 else tails[-1]


def N_ray(ray, *, eta_0: float = 0.05) -> float:
    """Intrinsic ray-tail cost from cross-level wedge and crosscut areas."""
    chains = build_attachment_chains(ray)
    if not chains:
        return 0.0
    total = sum(d.defect for d in ray.data) or 1.0
    tail_fracs = [c.intrinsic_tail_area / total for c in chains]
    return min(tail_fracs[-2:]) if len(tail_fracs) >= 2 else tail_fracs[0]


def N_tree(tree: CanonicalIntrusionTree, *, eta_0: float = 0.06) -> float:
    """inf_F liminf_N mu_sig(T \\ F_N)."""
    sig = build_signature_measure(tree)
    total = sig.total_mass or 1.0
    exhaust = audit_exhaustion(tree, max_N=min(8, tree.depth + 2))
    tail_fracs: list[float] = []
    for trunc in exhaust.truncations:
        unproc = [n for n in tree.nodes if n not in trunc.node_ids]
        mass_map = {s.node_id: s.s_local for s in sig.nodes}
        tail_fracs.append(sum(mass_map.get(n, 0.0) for n in unproc) / total)
    if not tail_fracs:
        return 0.0
    return min(tail_fracs[-2:]) if len(tail_fracs) >= 2 else tail_fracs[0]


def audit_intrinsic_tree_nonsummability(
    tree: CanonicalIntrusionTree,
    *,
    eta_child: float = 0.02,
    eta_ray: float = 0.05,
    eta_tree: float = 0.06,
) -> IntrinsicTreeNonsummabilityAudit:
    child_records: list[ChildNonsummabilityRecord] = []
    for nid, node in tree.nodes.items():
        if len(node.child_ids) < 4:
            continue
        fam = extract_countable_family(tree, nid)
        if not fam:
            continue
        L = L_v(fam.children)
        nc = N_child(len(fam.children), lambda N: tau_v(fam.children, N), eta_0=eta_child)
        linear = L > 2.5 or (L > 0 and nc >= eta_child * L)
        cross = nc >= eta_child and L > 1.0
        child_records.append(ChildNonsummabilityRecord(nid, nc, L, linear, cross))

    ray = extract_ray(tree)
    ray_rec: RayNonsummabilityRecord | None = None
    if ray:
        mass = ray_scale_mass(ray)
        nr = N_ray(ray, eta_0=eta_ray)
        ray_rec = RayNonsummabilityRecord(
            mass.S_ray,
            nr * (sum(d.defect for d in ray.data) or 1.0),
            nr,
            nr >= eta_ray or not mass.summable_ray,
        )

    nt = N_tree(tree, eta_0=eta_tree)
    tree_rec = TreeNonsummabilityRecord(nt, nt, nt >= eta_tree)

    failures: list[str] = []
    if any(c.linear_nonsummable for c in child_records):
        failures.append("CHILD_LINEAR")
    if any(c.cross_nonsummable for c in child_records):
        failures.append("CHILD_CROSS")
    if ray_rec and ray_rec.nonsummable:
        failures.append("RAY")
    if tree_rec.nonsummable:
        failures.append("TREE")

    fc: TreeFailureClass = "NONE"
    if len(failures) >= 2:
        fc = "MULTIPLE_TREE_FAILURES"
    elif "CHILD_LINEAR" in failures:
        fc = "CHILD_LINEAR_NONSUMMABILITY"
    elif "CHILD_CROSS" in failures:
        fc = "CHILD_CROSS_SIGNATURE_NONSUMMABILITY"
    elif "RAY" in failures:
        fc = "RAY_SIGNATURE_NONSUMMABILITY"
    elif tree_rec.nonsummable:
        fc = "DIFFUSE_END_NONSUMMABILITY"

    summ: SummabilityStatus = "SUMMABLE"
    if failures:
        summ = "MIXED" if len(failures) >= 2 else "NONSUMMABLE"

    return IntrinsicTreeNonsummabilityAudit(
        child_records=child_records,
        ray_record=ray_rec,
        tree_record=tree_rec,
        failure_class=fc,
        summability=summ,
        messages=[f"failure={fc}, summability={summ}, failures={failures}"],
    )
