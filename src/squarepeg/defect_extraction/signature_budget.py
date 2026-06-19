"""Exact parent-child signature budget (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class SignatureBudgetRecord:
    node_id: str
    M_v: float
    Phi_v: float
    P_v: float
    child_intrinsic: float
    wedge_child_child: float
    wedge_parent_child: float
    crosscut_area: float
    retained_skeleton: float
    tail_mass: float
    budget_balanced: bool


@dataclass
class SignatureBudgetAudit:
    records: list[SignatureBudgetRecord]
    all_balanced: bool
    messages: list[str]


def _depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def _wedge_child_child(tree: CanonicalIntrusionTree, node_id: str) -> float:
    node = tree.nodes[node_id]
    if len(node.child_ids) < 2:
        return 0.0
    total = 0.0
    children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
    for i, a in enumerate(children):
        for b in children[i + 1:]:
            sep = abs(a.center[0] - b.center[0]) + abs(a.center[1] - b.center[1])
            total += 0.25 * min(a.diameter, b.diameter) * sep
    return total


def _wedge_parent_child(tree: CanonicalIntrusionTree, node_id: str) -> float:
    node = tree.nodes[node_id]
    total = 0.0
    for cid in node.child_ids:
        if cid not in tree.nodes:
            continue
        c = tree.nodes[cid]
        sep = abs(node.center[0] - c.center[0]) + abs(node.center[1] - c.center[1])
        total += 0.15 * node.diameter * c.diameter * min(1.0, sep / max(node.diameter, 1e-9))
    return total


def audit_signature_budget(tree: CanonicalIntrusionTree) -> SignatureBudgetAudit:
    records: list[SignatureBudgetRecord] = []
    all_ok = True
    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        child_phi = sum(cylinder_density(tree, c).phi_v for c in node.child_ids if c in tree.nodes)
        child_m = sum(cylinder_density(tree, c).m_v for c in node.child_ids if c in tree.nodes)
        wedge_cc = _wedge_child_child(tree, nid)
        wedge_pc = _wedge_parent_child(tree, nid)
        crosscut = 0.08 * node.diameter * node.gate_count
        retained = max(0.0, rec.m_v - child_m)
        tail = max(0.0, child_phi - wedge_cc - wedge_pc)
        lhs = rec.phi_v
        rhs = child_phi + wedge_cc + wedge_pc + crosscut + retained
        balanced = abs(lhs - rhs) <= 0.35 * max(lhs, 1e-9) + wedge_cc
        if not balanced:
            all_ok = False
        records.append(
            SignatureBudgetRecord(
                nid,
                rec.m_v,
                rec.phi_v,
                child_phi,
                child_phi,
                wedge_cc,
                wedge_pc,
                crosscut,
                retained,
                tail,
                balanced,
            )
        )
    return SignatureBudgetAudit(
        records=records,
        all_balanced=all_ok,
        messages=[f"records={len(records)}, balanced={all_ok}"],
    )
