"""Child signature packing inequality (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

PackingStatus = Literal[
    "STRICT_CONTRACTION",
    "LOOSE_CONTRACTION",
    "NO_CONTRACTION",
    "GEOMETRICALLY_DERIVED",
]


@dataclass
class ChildPackingRecord:
    node_id: str
    phi_v: float
    child_phi_sum: float
    ratio: float
    theta_valid: float
    wedge_bound: float
    holds_strict: bool


@dataclass
class ChildSignaturePackingAudit:
    records: list[ChildPackingRecord]
    status: PackingStatus
    uniform_theta: float
    geometrically_derived: bool
    messages: list[str]


def _wedge_interaction_bound(tree: CanonicalIntrusionTree, node_id: str) -> float:
    node = tree.nodes[node_id]
    if len(node.child_ids) < 2:
        return 0.0
    centers = [tree.nodes[c].center for c in node.child_ids if c in tree.nodes]
    sep = 0.0
    for i, a in enumerate(centers):
        for b in centers[i + 1:]:
            sep = max(sep, abs(a[0] - b[0]) + abs(a[1] - b[1]))
    r = node.diameter
    return min(0.5 * r * r, 0.25 * sep * r)


def audit_child_signature_packing(tree: CanonicalIntrusionTree) -> ChildSignaturePackingAudit:
    records: list[ChildPackingRecord] = []
    strict_all = True
    loose_all = True
    derived = True
    thetas: list[float] = []

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        child_phi = sum(cylinder_density(tree, c).phi_v for c in node.child_ids if c in tree.nodes)
        wedge = _wedge_interaction_bound(tree, nid)
        ratio = child_phi / rec.phi_v if rec.phi_v > 1e-12 else 0.0
        theta = 1.0 - wedge / max(rec.phi_v, 1e-12)
        theta = max(0.5, min(theta, 1.0))
        thetas.append(theta)
        holds = child_phi <= theta * rec.phi_v + 1e-9 if rec.phi_v > 0 else True
        holds_strict = child_phi <= (theta - 0.05) * rec.phi_v + 1e-9 if rec.phi_v > 0 else True
        if not holds:
            loose_all = False
            derived = False
        if not holds_strict:
            strict_all = False
        records.append(
            ChildPackingRecord(nid, rec.phi_v, child_phi, ratio, theta, wedge, holds_strict)
        )

    status: PackingStatus = "NO_CONTRACTION"
    if strict_all and records:
        status = "STRICT_CONTRACTION"
    elif loose_all and records:
        status = "LOOSE_CONTRACTION"
    elif derived:
        status = "GEOMETRICALLY_DERIVED"

    uniform = sum(thetas) / len(thetas) if thetas else 1.0
    return ChildSignaturePackingAudit(
        records=records,
        status=status,
        uniform_theta=uniform,
        geometrically_derived=derived,
        messages=[f"status={status}, theta~={uniform:.3f}, strict={strict_all}"],
    )
