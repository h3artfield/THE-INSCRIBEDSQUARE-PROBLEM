"""Intrinsic non-Carleson end density (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_signature_measure import end_sig_mass, phi_end_scale
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.intrusion_tree_boundary import build_tree_boundary

NonCarlesonClass = Literal[
    "ZERO_SCALE_POSITIVE_MASS",
    "UNBOUNDED_END_DENSITY",
    "PERSISTENT_END_DENSITY",
    "NONUNIFORM_CARLESON_TAIL",
    "MULTIPLE_END_FAILURES",
    "CARLESON_SATISFIED",
]


@dataclass
class CylinderDensityRecord:
    node_id: str
    m_v: float
    phi_v: float
    D_v: float
    depth: int
    zero_scale_positive: bool


@dataclass
class NonCarlesonEndDensityAudit:
    records: list[CylinderDensityRecord]
    D_N_sup: float
    failure_class: NonCarlesonClass
    intrinsically_non_carleson: bool
    eta_0: float
    messages: list[str]


def _depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def cylinder_density(tree: CanonicalIntrusionTree, node_id: str) -> CylinderDensityRecord:
    m = end_sig_mass(tree, node_id)
    phi = phi_end_scale(tree, node_id)
    zero = phi <= 1e-12 and m > 1e-9
    D = m / phi if phi > 1e-12 else float("inf") if m > 1e-9 else 0.0
    return CylinderDensityRecord(node_id, m, phi, D, _depth(tree, node_id), zero)


def deep_density_sup(tree: CanonicalIntrusionTree, *, min_depth: int = 2) -> float:
    records = [cylinder_density(tree, nid) for nid in tree.nodes if tree.nodes[nid].child_ids or not tree.nodes[nid].parent_id]
    deep = [r.D_v for r in records if r.depth >= min_depth and r.phi_v > 1e-12]
    return max(deep, default=0.0)


def audit_noncarleson_end_density(
    tree: CanonicalIntrusionTree,
    *,
    eta_0: float = 0.35,
    A_bound: float = 10.0,
) -> NonCarlesonEndDensityAudit:
    carl = audit_end_signature_carleson(tree)
    records = [cylinder_density(tree, nid) for nid in tree.nodes if nid in tree.nodes]
    D_sup = deep_density_sup(tree)
    zero_scale = any(r.zero_scale_positive for r in records)
    unbounded = D_sup >= A_bound or any(r.D_v == float("inf") for r in records)
    persistent = D_sup >= eta_0 and not carl.vanishing_fine_tails
    nonuniform = not carl.satisfies_carleson and carl.cylinder_bounded

    fc: NonCarlesonClass = "CARLESON_SATISFIED"
    if carl.satisfies_carleson:
        fc = "CARLESON_SATISFIED"
    elif zero_scale:
        fc = "ZERO_SCALE_POSITIVE_MASS"
    elif unbounded:
        fc = "UNBOUNDED_END_DENSITY"
    elif persistent:
        fc = "PERSISTENT_END_DENSITY"
    elif nonuniform:
        fc = "NONUNIFORM_CARLESON_TAIL"
    elif zero_scale and persistent:
        fc = "MULTIPLE_END_FAILURES"

    non_carleson = fc != "CARLESON_SATISFIED"
    return NonCarlesonEndDensityAudit(
        records=records,
        D_N_sup=D_sup,
        failure_class=fc,
        intrinsically_non_carleson=non_carleson,
        eta_0=eta_0,
        messages=[f"class={fc}, D_sup={D_sup:.3f}, non_carleson={non_carleson}"],
    )
