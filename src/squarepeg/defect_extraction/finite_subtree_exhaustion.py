"""Finite subtree surgery exhaustion (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree


@dataclass
class SurgeryNodeRecord:
    node_id: str
    diameter: float
    defect: float
    gate_count: int
    sigma_v: float
    t051_applicable: bool
    t080_ray_tail: bool
    jordan_hull: bool


@dataclass
class FiniteSubtree:
    N: int
    eta_N: float
    node_ids: list[str]
    maximal_surgery_nodes: list[str]
    jordan_preserved: bool
    crosscuts_disjoint: bool


@dataclass
class ExhaustionAudit:
    truncations: list[FiniteSubtree]
    monotone_inclusion: bool
    uniform_closeness: float
    messages: list[str]


def _depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def build_truncation(tree: CanonicalIntrusionTree, N: int, *, eta: float | None = None) -> FiniteSubtree:
    """F_N = {v : depth(v) <= N, r_v >= eta_N}."""
    eta_N = eta if eta is not None else max(0.01, 1.0 / (N + 2))
    ids = [nid for nid, n in tree.nodes.items() if _depth(tree, nid) <= N and n.diameter >= eta_N]
    maximal: list[str] = []
    id_set = set(ids)
    for nid in ids:
        node = tree.nodes[nid]
        if node.child_ids and any(c in id_set for c in node.child_ids):
            maximal.append(nid)
    return FiniteSubtree(
        N=N,
        eta_N=eta_N,
        node_ids=ids,
        maximal_surgery_nodes=maximal,
        jordan_preserved=all(tree.nodes[n].jordan_hull for n in ids),
        crosscuts_disjoint=True,
    )


def audit_exhaustion(tree: CanonicalIntrusionTree, *, max_N: int = 8) -> ExhaustionAudit:
    truncs = [build_truncation(tree, N, eta=0.05 / (N + 1)) for N in range(2, max_N + 1)]
    monotone = all(set(truncs[i].node_ids) <= set(truncs[i + 1].node_ids) for i in range(len(truncs) - 1))
    if truncs:
        last = truncs[-1]
        unprocessed = [n for n in tree.nodes if n not in last.node_ids]
        uniform = max((tree.nodes[n].diameter for n in unprocessed), default=0.0)
    else:
        uniform = 0.0
    return ExhaustionAudit(
        truncations=truncs,
        monotone_inclusion=monotone,
        uniform_closeness=uniform,
        messages=[f"truncs={len(truncs)}, monotone={monotone}, tail_r={uniform:.4f}"],
    )


def node_surgery_records(tree: CanonicalIntrusionTree) -> list[SurgeryNodeRecord]:
    from squarepeg.defect_extraction.tree_signature_measure import node_signature_weight

    records: list[SurgeryNodeRecord] = []
    for nid, node in tree.nodes.items():
        children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
        sigma = node_signature_weight(node, children)
        records.append(
            SurgeryNodeRecord(
                node_id=nid,
                diameter=node.diameter,
                defect=node.defect,
                gate_count=node.gate_count,
                sigma_v=sigma,
                t051_applicable=node.gate_class == "TWO_GATE" and node.jordan_hull,
                t080_ray_tail=len(children) == 1 and node.gate_count == 2,
                jordan_hull=node.jordan_hull,
            )
        )
    return records
