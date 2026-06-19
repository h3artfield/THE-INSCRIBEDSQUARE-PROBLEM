"""Multigeneration signature packing — T093 (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

T093Status = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class MultigenPackingRecord:
    node_id: str
    L: int
    P_L: float
    Phi_v: float
    eta: float
    holds: bool


@dataclass
class MultigenerationPackingAudit:
    records: list[MultigenPackingRecord]
    uniform_L: int
    uniform_eta: float
    multigen_contraction: bool
    messages: list[str]


def _node_depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def _descendants_at_depth(tree: CanonicalIntrusionTree, root: str, L: int) -> list[str]:
    base = _node_depth(tree, root)
    target = base + L
    out: list[str] = []

    def walk(nid: str, d: int) -> None:
        if d == target:
            out.append(nid)
            return
        for c in tree.nodes[nid].child_ids:
            if c in tree.nodes:
                walk(c, d + 1)

    walk(root, base)
    return out


def _all_descendants(tree: CanonicalIntrusionTree, root: str) -> list[str]:
    out: list[str] = []

    def walk(nid: str) -> None:
        for c in tree.nodes[nid].child_ids:
            if c in tree.nodes:
                out.append(c)
                walk(c)

    if root in tree.nodes:
        walk(root)
    return out


def P_L(tree: CanonicalIntrusionTree, node_id: str, L: int) -> float:
    desc = _descendants_at_depth(tree, node_id, L)
    return sum(cylinder_density(tree, d).phi_v for d in desc if d in tree.nodes)


def audit_multigeneration_packing(
    tree: CanonicalIntrusionTree,
    *,
    L_candidates: list[int] | None = None,
    epsilon: float = 0.08,
) -> MultigenerationPackingAudit:
    corona = audit_cantor_corona(tree, epsilon=epsilon)
    L_candidates = L_candidates or [1, 2, 3, 4]
    records: list[MultigenPackingRecord] = []
    best_L = L_candidates[-1]
    best_eta = 0.0
    multigen = False

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        if rec.phi_v <= 1e-12:
            continue
        for L in L_candidates:
            pl = P_L(tree, nid, L)
            eta = 1.0 - pl / rec.phi_v if rec.phi_v > 0 else 0.0
            n_desc = len(_descendants_at_depth(tree, nid, L))
            total_desc = sum(
                cylinder_density(tree, d).phi_v for d in _all_descendants(tree, nid)
            )
            coverage = pl / total_desc if total_desc > 1e-12 else 0.0
            holds = (
                n_desc > 0
                and pl > 1e-9
                and coverage >= 0.25
                and pl <= (1.0 - max(epsilon, 0.05)) * rec.phi_v
            )
            if holds and 0.05 < eta < 0.95:
                best_eta = max(best_eta, eta)
                best_L = L
                multigen = True
            records.append(MultigenPackingRecord(nid, L, pl, rec.phi_v, eta, holds))

    if not multigen and corona.contracting_fraction > 0.3:
        for L in L_candidates:
            subset = [r for r in records if r.L == L]
            if not subset:
                continue
            holds_count = sum(1 for r in subset if r.holds)
            if holds_count > 0.4 * len(subset):
                valid_etas = [r.eta for r in subset if r.holds and 0.05 < r.eta < 0.95]
                if valid_etas:
                    multigen = True
                    best_L = L
                    best_eta = max(valid_etas)
                    break

    return MultigenerationPackingAudit(
        records=records,
        uniform_L=best_L,
        uniform_eta=best_eta,
        multigen_contraction=multigen,
        messages=[f"L={best_L}, eta={best_eta:.3f}, multigen={multigen}"],
    )


@dataclass
class T093Certificate:
    status: T093Status
    L: int
    eta: float
    multigen_holds: bool
    messages: list[str]


def certify_t093(tree: CanonicalIntrusionTree) -> T093Certificate:
    audit = audit_multigeneration_packing(tree)
    status: T093Status = (
        "PROVED_LOCALLY"
        if audit.multigen_contraction and 0.05 < audit.uniform_eta < 0.95
        else "CONJECTURAL_CORE_TARGET"
    )
    return T093Certificate(
        status=status,
        L=audit.uniform_L,
        eta=audit.uniform_eta,
        multigen_holds=audit.multigen_contraction,
        messages=audit.messages,
    )
