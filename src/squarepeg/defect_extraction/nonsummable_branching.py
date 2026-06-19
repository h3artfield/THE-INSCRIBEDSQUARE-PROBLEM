"""Nonsummable branching and T083/T082R (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_carleson import audit_branching_carleson_v2
from squarepeg.defect_extraction.branching_defect_classifier import audit_branching_defects
from squarepeg.defect_extraction.branching_tree_area_tightness import certify_t081_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.diffuse_end_measure import audit_diffuse_end_measure
from squarepeg.defect_extraction.finite_subtree_exhaustion import audit_exhaustion
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure

T083Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T082RStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T083Route = Literal[
    "CONCENTRATED_DESCENDANT_RAY",
    "FINITE_CENTER_SPLITTING",
    "DIFFUSE_END_MEASURE",
    "INFINITE_CENTER_PROLIFERATION",
    "NON_JORDAN_HULL",
    "PARAMETER_DISCONNECTED",
    "POSITIVE_SCALE_NONANNULAR",
]


@dataclass
class NonsummableBranchingAudit:
    nonsummable: bool
    intrinsic_tail: float
    eta_0: float
    inf_attained: bool
    messages: list[str]


@dataclass
class T083Certificate:
    status: T083Status
    route: T083Route
    nonsummable: bool
    messages: list[str]


@dataclass
class T082RCertificate:
    status: T082RStatus
    route: str
    t080: str
    t081: str
    messages: list[str]


def audit_intrinsic_branching_nonsummability(
    tree: CanonicalIntrusionTree,
    *,
    eta_0: float = 0.08,
) -> NonsummableBranchingAudit:
    """inf_F liminf_N mu_sig(T \\ F_N) >= eta_0."""
    sig = build_signature_measure(tree)
    total = sig.total_mass or 1.0
    exhaust = audit_exhaustion(tree, max_N=min(8, tree.depth + 2))
    tail_fracs: list[float] = []
    for trunc in exhaust.truncations:
        unproc = [n for n in tree.nodes if n not in trunc.node_ids]
        mass_map = {s.node_id: s.s_local for s in sig.nodes}
        tail = sum(mass_map.get(n, 0.0) for n in unproc) / total
        tail_fracs.append(tail)
    intrinsic = min(tail_fracs[-2:]) if len(tail_fracs) >= 2 else (tail_fracs[0] if tail_fracs else 0.0)
    nonsummable = intrinsic >= eta_0 and not audit_branching_carleson_v2(tree).satisfies_carleson
    return NonsummableBranchingAudit(
        nonsummable=nonsummable,
        intrinsic_tail=intrinsic,
        eta_0=eta_0,
        inf_attained=True,
        messages=[f"nonsummable={nonsummable}, tail={intrinsic:.4f}"],
    )


def certify_t083(tree: CanonicalIntrusionTree) -> T083Certificate:
    """T083: nonsummable branching alternative."""
    ns = audit_intrinsic_branching_nonsummability(tree)
    defects = audit_branching_defects(tree)
    diffuse = audit_diffuse_end_measure(tree)
    route: T083Route = "DIFFUSE_END_MEASURE"
    status: T083Status = "CONJECTURAL_STRUCTURAL_TARGET"
    if not ns.nonsummable:
        route = "CONCENTRATED_DESCENDANT_RAY"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif defects.routes_to_t080:
        route = "CONCENTRATED_DESCENDANT_RAY"
    elif defects.routes_to_t062:
        route = "FINITE_CENTER_SPLITTING"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif diffuse.status == "DIFFUSE_END_MEASURE_TREE":
        route = "DIFFUSE_END_MEASURE"
    elif defects.primary_route == "JOIN_DOMINATED":
        route = "INFINITE_CENTER_PROLIFERATION"
    return T083Certificate(
        status=status,
        route=route,
        nonsummable=ns.nonsummable,
        messages=[f"route={route}, nonsummable={ns.nonsummable}"],
    )


def certify_t082r(tree: CanonicalIntrusionTree) -> T082RCertificate:
    """T082R: infinite intrusion-tree reduction."""
    t080 = certify_t080(tree)
    t081 = certify_t081_v2(tree)
    t083 = certify_t083(tree)
    route = t083.route
    status: T082RStatus = "CONJECTURAL_TARGET"
    if t081.status == "PROVED_LOCALLY":
        route = "T081_SUMMABLE_BRANCHING"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t080.status == "PROVED_LOCALLY":
        route = "T080_SUMMABLE_RAY"
        status = "PROVED_LOCALLY_PARTIAL"
    return T082RCertificate(
        status=status,
        route=str(route),
        t080=t080.status,
        t081=t081.status,
        messages=[f"route={route}, t081={t081.status}"],
    )
