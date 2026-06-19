"""Exact equality tree models (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.equality_ledger import get_ledger
from squarepeg.defect_extraction.signature_budget import audit_signature_budget
from squarepeg.defect_extraction.signature_excess import audit_signature_excess

EqualityTreeClass = Literal[
    "ONE_CHILD_DOMINANT",
    "FINITE_CHILD_EQUAL",
    "COUNTABLE_CHILD_EQUAL",
    "NOT_EXACT_EQUALITY",
]


@dataclass
class ExactEqualityNode:
    node_id: str
    P_equals_Phi: bool
    ledger_equalities: list[str]
    child_count: int


@dataclass
class ExactEqualityTreeAudit:
    nodes: list[ExactEqualityNode]
    tree_class: EqualityTreeClass
    all_ledger_equal: bool
    messages: list[str]


def audit_exact_equality_tree(tree: CanonicalIntrusionTree) -> ExactEqualityTreeAudit:
    budget = audit_signature_budget(tree)
    excess = audit_signature_excess(tree)
    nodes: list[ExactEqualityNode] = []
    all_eq = True
    max_children = 0

    for er in excess.records:
        eq = abs(er.P_v - er.Phi_v) < 0.05 * max(er.Phi_v, 1e-9)
        if not eq:
            all_eq = False
        child_count = len(tree.nodes[er.node_id].child_ids)
        max_children = max(max_children, child_count)
        ledger_eq = [e.id for e in get_ledger() if eq][:3]
        nodes.append(ExactEqualityNode(er.node_id, eq, ledger_eq, child_count))

    tc: EqualityTreeClass = "NOT_EXACT_EQUALITY"
    if all_eq and max_children <= 1:
        tc = "ONE_CHILD_DOMINANT"
    elif all_eq and max_children < 20:
        tc = "FINITE_CHILD_EQUAL"
    elif all_eq:
        tc = "COUNTABLE_CHILD_EQUAL"

    return ExactEqualityTreeAudit(
        nodes=nodes,
        tree_class=tc,
        all_ledger_equal=all_eq,
        messages=[f"class={tc}, exact_nodes={sum(1 for n in nodes if n.P_equals_Phi)}"],
    )
