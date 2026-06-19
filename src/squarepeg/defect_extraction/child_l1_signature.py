"""CHILD_L1_SIGNATURE — full definition (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.countable_child_identity import audit_countable_child_identity, L_v, tau_v
from squarepeg.defect_extraction.countable_child_order import extract_countable_family, delta_increment


@dataclass
class NodeL1Certificate:
    node_id: str
    L_v: float
    tau_vanishes: bool
    geometric_sufficient: bool
    jordan_preserved: bool
    satisfies_l1: bool


@dataclass
class ChildL1SignatureAudit:
    nodes: list[NodeL1Certificate]
    global_l1: bool
    uniform_local: bool
    messages: list[str]


def geometric_child_mass(records) -> float:
    return sum(r.gate_count * r.diameter for r in records)


def audit_child_l1_signature_v2(
    tree: CanonicalIntrusionTree,
    *,
    tail_threshold: float = 0.25,
    C_gate: float = 0.15,
) -> ChildL1SignatureAudit:
    """CHILD_L1_SIGNATURE at every countably branching node."""
    certs: list[NodeL1Certificate] = []
    for nid, node in tree.nodes.items():
        children_ids = node.child_ids
        if len(children_ids) < 2:
            continue
        family = extract_countable_family(tree, nid)
        if not family:
            continue
        recs = family.children
        L = L_v(recs)
        N = max(4, len(recs) // 4)
        tau = tau_v(recs, N)
        geom = geometric_child_mass(recs)
        geom_ok = geom < 5.0 and all(
            rec.delta_norm <= C_gate * rec.gate_count * rec.diameter + 1e-9 for rec in recs
        )
        tau_ok = tau < tail_threshold * L if L > 0 else True
        jordan = node.jordan_hull and all(tree.nodes[c].jordan_hull for c in children_ids if c in tree.nodes)
        identity = audit_countable_child_identity(family)
        satisfies = L < 20.0 and tau_ok and identity.tail.absolute_convergence and jordan
        if geom_ok and geom < 3.0:
            satisfies = satisfies or (tau_ok and jordan)
        certs.append(
            NodeL1Certificate(
                node_id=nid,
                L_v=L,
                tau_vanishes=tau_ok,
                geometric_sufficient=geom_ok and geom < 3.0,
                jordan_preserved=jordan,
                satisfies_l1=satisfies,
            )
        )
    global_l1 = all(c.satisfies_l1 for c in certs) if certs else True
    uniform = all(c.tau_vanishes for c in certs) if certs else True
    return ChildL1SignatureAudit(
        nodes=certs,
        global_l1=global_l1,
        uniform_local=uniform,
        messages=[f"global_l1={global_l1}, nodes={len(certs)}"],
    )


def L_J_v(tree: CanonicalIntrusionTree, parent_id: str, *, delta: float = 0.1) -> float:
    """Uniform local L_J(v) for short intervals."""
    family = extract_countable_family(tree, parent_id)
    if not family:
        return 0.0
    return sum(r.delta_norm for r in family.children if r.param_interval[1] - r.param_interval[0] <= delta + 0.5)
