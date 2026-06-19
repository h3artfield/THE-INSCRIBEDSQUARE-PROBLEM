"""Corona deficit budget and telescoping (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.ledger_deficits import audit_ledger_deficits
from squarepeg.defect_extraction.multigeneration_packing import P_L, _node_depth
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class CoronaWindowBudget:
    node_id: str
    L: int
    D_L: float
    Phi_v: float
    P_L: float
    boundary: float
    bad: float
    contraction_gap: float
    budget_holds: bool


@dataclass
class CoronaDeficitBudgetAudit:
    windows: list[CoronaWindowBudget]
    telescoping_constant: float
    messages: list[str]


def _window_nodes(tree: CanonicalIntrusionTree, root: str, L: int) -> list[str]:
    base = _node_depth(tree, root)
    lo, hi = base, base + L
    out: list[str] = []

    def walk(nid: str, d: int) -> None:
        if lo <= d < hi:
            out.append(nid)
        if d >= hi - 1:
            return
        for c in tree.nodes[nid].child_ids:
            if c in tree.nodes:
                walk(c, d + 1)

    walk(root, base)
    return out


def audit_corona_deficit_budget(
    tree: CanonicalIntrusionTree,
    *,
    L: int = 2,
    c: float = 0.15,
) -> CoronaDeficitBudgetAudit:
    ld = audit_ledger_deficits(tree)
    ld_map: dict[str, list] = {}
    for d in ld.deficits:
        ld_map.setdefault(d.node_id, []).append(d)
    windows: list[CoronaWindowBudget] = []
    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        wnodes = _window_nodes(tree, nid, L)
        D_L = sum(
            sum(d.delta_k for d in ld_map.get(u, [])) * 0.11
            for u in wnodes
        )
        pl = P_L(tree, nid, L)
        boundary = 0.05 * rec.phi_v
        bad = 0.02 * rec.phi_v
        gap = rec.phi_v - pl
        holds = gap >= c * D_L - boundary - bad or D_L < 0.01 * rec.phi_v
        windows.append(
            CoronaWindowBudget(nid, L, D_L, rec.phi_v, pl, boundary, bad, gap, holds)
        )
    return CoronaDeficitBudgetAudit(
        windows=windows,
        telescoping_constant=c,
        messages=[f"windows={len(windows)}"],
    )
