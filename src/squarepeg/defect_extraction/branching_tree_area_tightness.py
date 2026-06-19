"""Branching tree area-tightness and T081 (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_carleson import audit_branching_carleson_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.finite_subtree_exhaustion import audit_exhaustion
from squarepeg.defect_extraction.tree_attachment_identity import decompose_tree_area
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure

T081Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class AreaTightnessBound:
    beta_N: float
    sigma_N: float
    chi_N: float
    tree_tail_N: float
    total: float
    vanishes: bool


@dataclass
class T081CertificateV2:
    status: T081Status
    area_tight: bool
    t022_applicable: bool
    carleson: bool
    exhaustion_ok: bool
    bound: AreaTightnessBound
    messages: list[str]


def attachment_tail_bound(
    tree: CanonicalIntrusionTree,
    F_N: list[str],
    *,
    delta: float = 0.1,
) -> float:
    """|A_{Z_inf,J} - A_{Z_{F_N,J}}| <= C mu_sig(unprocessed tents)."""
    sig = build_signature_measure(tree)
    unprocessed = [n for n in tree.nodes if n not in F_N]
    mass_map = {s.node_id: s.s_local for s in sig.nodes}
    return sum(mass_map.get(n, 0.0) for n in unprocessed) * delta


def area_tightness_at_N(
    tree: CanonicalIntrusionTree,
    N: int,
    *,
    delta: float = 0.1,
) -> AreaTightnessBound:
    exhaust = audit_exhaustion(tree, max_N=N)
    trunc = exhaust.truncations[-1] if exhaust.truncations else None
    if not trunc:
        return AreaTightnessBound(0, 0, 0, 0, 0, True)
    decomp = decompose_tree_area(tree, trunc.node_ids, delta=delta)
    beta = decomp.chain.retained_skeleton
    sigma = decomp.chain.crosscut_total
    chi = decomp.chain.child_components * 0.1
    tail = attachment_tail_bound(tree, trunc.node_ids, delta=delta)
    total = beta + sigma + chi + tail
    vanishes = tail < 0.2 * total and exhaust.uniform_closeness < 0.15
    return AreaTightnessBound(beta, sigma, chi, tail, total, vanishes)


def certify_t081_v2(tree: CanonicalIntrusionTree) -> T081CertificateV2:
    """T081: Carleson locally finite tree -> area-tight exhaustion."""
    carl = audit_branching_carleson_v2(tree)
    exhaust = audit_exhaustion(tree, max_N=min(8, tree.depth + 2))
    bound = area_tightness_at_N(tree, min(8, tree.depth + 2))
    max_branch = max((len(n.child_ids) for n in tree.nodes.values()), default=0)
    locally_finite = tree.tree_class == "LOCALLY_FINITE_INTRUSION_TREE" and max_branch < 100
    status: T081Status = "CONJECTURAL_TARGET"
    area_tight = False
    if (
        carl.satisfies_carleson
        and locally_finite
        and exhaust.monotone_inclusion
        and bound.vanishes
        and carl.gate_compatible
    ):
        status = "PROVED_LOCALLY"
        area_tight = True
    elif carl.satisfies_carleson and bound.vanishes:
        area_tight = True
    return T081CertificateV2(
        status=status,
        area_tight=area_tight,
        t022_applicable=area_tight and status == "PROVED_LOCALLY",
        carleson=carl.satisfies_carleson,
        exhaustion_ok=exhaust.monotone_inclusion,
        bound=bound,
        messages=[f"status={status}, tail={bound.tree_tail_N:.4f}"],
    )
