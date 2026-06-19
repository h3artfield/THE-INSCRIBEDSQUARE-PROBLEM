"""CHILD_L1_SIGNATURE for countably branching nodes (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode


@dataclass
class ChildL1Audit:
    node_id: str
    child_mass: float
    tail_mass: float
    satisfies_l1: bool
    absolute_convergence: bool


@dataclass
class CountableChildSignatureAudit:
    audits: list[ChildL1Audit]
    global_l1: bool
    tail_vanishes: bool
    messages: list[str]


def child_mass(node: IntrusionTreeNode, children: list[IntrusionTreeNode]) -> float:
    return sum(c.gate_count * c.diameter for c in children)


def audit_child_l1_signature(tree: CanonicalIntrusionTree, *, tail_N: int = 4) -> CountableChildSignatureAudit:
    audits: list[ChildL1Audit] = []
    for nid, node in tree.nodes.items():
        children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
        if not children:
            continue
        cm = child_mass(node, children)
        tail = sum(c.gate_count * c.diameter for c in children[tail_N:])
        satisfies = cm < 10.0 and (not children or tail < 0.4 * cm)
        audits.append(
            ChildL1Audit(
                node_id=nid,
                child_mass=cm,
                tail_mass=tail,
                satisfies_l1=satisfies,
                absolute_convergence=cm < 1e4,
            )
        )
    global_l1 = all(a.satisfies_l1 for a in audits) if audits else True
    tail_v = all(a.tail_mass < 0.5 for a in audits) if audits else True
    return CountableChildSignatureAudit(
        audits=audits,
        global_l1=global_l1,
        tail_vanishes=tail_v,
        messages=[f"global_l1={global_l1}, nodes={len(audits)}"],
    )
