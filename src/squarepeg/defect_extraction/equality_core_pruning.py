"""Equality-core pruning by signature scale (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.corona_deficit_budget import audit_corona_deficit_budget
from squarepeg.defect_extraction.ledger_deficits import audit_ledger_deficits
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class GoodNodeRecord:
    node_id: str
    max_d_k: float
    phi: float
    is_good: bool


@dataclass
class EqualityCorePruningAudit:
    good_nodes: list[GoodNodeRecord]
    bad_signature_mass: float
    good_signature_mass: float
    markov_bound: float
    epsilon: float
    messages: list[str]


def audit_equality_core_pruning(
    tree: CanonicalIntrusionTree,
    *,
    epsilon: float = 0.1,
    L: int = 2,
) -> EqualityCorePruningAudit:
    ld = audit_ledger_deficits(tree)
    budget = audit_corona_deficit_budget(tree, L=L)
    good: list[GoodNodeRecord] = []
    good_phi = 0.0
    bad_phi = 0.0
    D_L_total = sum(w.D_L for w in budget.windows)

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        node_d = [d for d in ld.deficits if d.node_id == nid]
        max_d = max((d.d_k for d in node_d), default=0.0)
        is_g = max_d <= epsilon
        good.append(GoodNodeRecord(nid, max_d, rec.phi_v, is_g))
        if is_g:
            good_phi += rec.phi_v
        else:
            bad_phi += rec.phi_v

    markov = (D_L_total / max(epsilon, 1e-9)) if epsilon > 0 else float("inf")
    return EqualityCorePruningAudit(
        good_nodes=good,
        bad_signature_mass=bad_phi,
        good_signature_mass=good_phi,
        markov_bound=markov,
        epsilon=epsilon,
        messages=[f"good_phi={good_phi:.3f}, bad_phi={bad_phi:.3f}, markov={markov:.3f}"],
    )
