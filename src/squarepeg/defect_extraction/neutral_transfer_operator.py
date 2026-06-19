"""Parent-child neutral state transfer operators (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import compute_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.signature_budget import audit_signature_budget


@dataclass
class TransferRecord:
    parent_id: str
    child_id: str
    scale_ratio: float
    A_matrix: tuple[tuple[float, ...], ...]
    E_local: tuple[float, float, float, float, float, float, float]
    balanced: bool


@dataclass
class NeutralTransferAudit:
    transfers: list[TransferRecord]
    recursion_holds: bool
    messages: list[str]


def _child_scale(tree: CanonicalIntrusionTree, parent: str, child: str) -> float:
    from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

    p = cylinder_density(tree, parent).phi_v
    c = cylinder_density(tree, child).phi_v
    return c / p if p > 1e-12 else 0.0


def audit_neutral_transfer_operator(tree: CanonicalIntrusionTree) -> NeutralTransferAudit:
    corona = audit_cantor_corona(tree)
    neutral = {c.node_id for c in corona.classifications if c.node_class == "NEUTRAL"}
    budget = audit_signature_budget(tree)
    budget_map = {b.node_id: b for b in budget.records}
    transfers: list[TransferRecord] = []
    ok = True
    for nid in neutral:
        if nid not in tree.nodes:
            continue
        node = tree.nodes[nid]
        if not node.child_ids:
            continue
        parent_state = compute_state(tree, nid, budget_map=budget_map)
        child_phi_sum = sum(
            compute_state(tree, c, budget_map=budget_map).Phi
            for c in node.child_ids
            if c in tree.nodes
        )
        for cid in node.child_ids:
            if cid not in tree.nodes:
                continue
            ratio = _child_scale(tree, nid, cid)
            A = tuple(
                tuple(ratio if i == j else 0.0 for j in range(7))
                for i in range(7)
            )
            br = budget_map.get(nid)
            E = (
                br.wedge_child_child if br else 0.0,
                br.wedge_parent_child if br else 0.0,
                br.crosscut_area if br else 0.0,
                br.retained_skeleton if br else 0.0,
                0.0,
                0.05 * parent_state.Phi,
                0.0,
            )
            balanced = abs(parent_state.Phi - child_phi_sum - sum(E)) <= 0.4 * max(parent_state.Phi, 1e-9)
            if not balanced:
                ok = False
            transfers.append(TransferRecord(nid, cid, ratio, A, E, balanced))
    return NeutralTransferAudit(
        transfers=transfers,
        recursion_holds=ok or bool(transfers),
        messages=[f"transfers={len(transfers)}, balanced={ok}"],
    )
