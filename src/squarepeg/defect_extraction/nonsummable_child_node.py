"""Nonsummable child nodes (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.countable_child_identity import L_v, tau_v
from squarepeg.defect_extraction.countable_child_order import CountableChildFamily, extract_countable_family
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree


@dataclass
class NonsummableChildAudit:
    node_id: str
    C_v_N: float
    nonsummable: bool
    eta_0: float


@dataclass
class IntrinsicChildTailAudit:
    audits: list[NonsummableChildAudit]
    any_nonsummable: bool
    messages: list[str]


def optimal_child_tail_cost(family: CountableChildFamily, N: int) -> float:
    """C_v(N) = inf over orderings; fixed geometric order here."""
    return tau_v(family.children, N)


def audit_nonsummable_child_nodes(
    tree: CanonicalIntrusionTree,
    *,
    eta_0: float = 0.05,
) -> IntrinsicChildTailAudit:
    audits: list[NonsummableChildAudit] = []
    for nid, node in tree.nodes.items():
        if len(node.child_ids) < 4:
            continue
        family = extract_countable_family(tree, nid)
        if not family:
            continue
        N = max(4, len(family.children) // 3)
        C = optimal_child_tail_cost(family, N)
        L = L_v(family.children)
        nonsummable = C >= eta_0 * L if L > 0 else False
        audits.append(NonsummableChildAudit(nid, C, nonsummable, eta_0))
    return IntrinsicChildTailAudit(
        audits=audits,
        any_nonsummable=any(a.nonsummable for a in audits),
        messages=[f"nonsummable={any(a.nonsummable for a in audits)}, nodes={len(audits)}"],
    )
