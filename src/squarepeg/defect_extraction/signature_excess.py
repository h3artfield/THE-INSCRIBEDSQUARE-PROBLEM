"""Signature packing excess decomposition (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.signature_budget import audit_signature_budget

ExcessMechanism = Literal[
    "CHILD_HULL_OVERLAP_EXCESS",
    "SHARED_GATE_EXCESS",
    "CENTER_DRIFT_EXCESS",
    "CROSS_CHILD_WEDGE_EXCESS",
    "THIN_CHILD_EXCESS",
    "RETAINED_SKELETON_EXCESS",
    "SIGN_CANCELLATION_EXCESS",
    "NONE",
]


@dataclass
class ExcessRecord:
    node_id: str
    Phi_v: float
    P_v: float
    E_frak: float
    mechanisms: list[ExcessMechanism]


@dataclass
class SignatureExcessAudit:
    records: list[ExcessRecord]
    total_excess: float
    dominant: ExcessMechanism
    messages: list[str]


def audit_signature_excess(tree: CanonicalIntrusionTree) -> SignatureExcessAudit:
    budget = audit_signature_budget(tree)
    records: list[ExcessRecord] = []
    totals: dict[ExcessMechanism, float] = {m: 0.0 for m in (
        "CHILD_HULL_OVERLAP_EXCESS",
        "SHARED_GATE_EXCESS",
        "CENTER_DRIFT_EXCESS",
        "CROSS_CHILD_WEDGE_EXCESS",
        "THIN_CHILD_EXCESS",
        "RETAINED_SKELETON_EXCESS",
        "SIGN_CANCELLATION_EXCESS",
    )}

    for br in budget.records:
        node = tree.nodes[br.node_id]
        E = max(0.0, br.P_v - br.Phi_v)
        mechs: list[ExcessMechanism] = []
        if br.wedge_child_child > 0.01 * br.Phi_v:
            mechs.append("CROSS_CHILD_WEDGE_EXCESS")
            totals["CROSS_CHILD_WEDGE_EXCESS"] += br.wedge_child_child
        if br.retained_skeleton > 0.01 * br.Phi_v:
            mechs.append("RETAINED_SKELETON_EXCESS")
            totals["RETAINED_SKELETON_EXCESS"] += br.retained_skeleton
        if br.wedge_parent_child > 0.01 * br.Phi_v:
            mechs.append("CHILD_HULL_OVERLAP_EXCESS")
            totals["CHILD_HULL_OVERLAP_EXCESS"] += br.wedge_parent_child
        if br.crosscut_area > 0.05 * br.Phi_v:
            mechs.append("SHARED_GATE_EXCESS")
            totals["SHARED_GATE_EXCESS"] += br.crosscut_area
        if node.child_ids:
            centers = [tree.nodes[c].center for c in node.child_ids if c in tree.nodes]
            drift = max(
                abs(a[0] - b[0]) + abs(a[1] - b[1])
                for i, a in enumerate(centers)
                for b in centers[i + 1:]
            ) if len(centers) > 1 else 0.0
            if drift > 0.1 * node.diameter:
                mechs.append("CENTER_DRIFT_EXCESS")
                totals["CENTER_DRIFT_EXCESS"] += drift * node.diameter
        signs = {tree.nodes[c].sign for c in node.child_ids if c in tree.nodes}
        if len(signs) > 1:
            mechs.append("SIGN_CANCELLATION_EXCESS")
            totals["SIGN_CANCELLATION_EXCESS"] += 0.05 * E
        thin = any(tree.nodes[c].diameter < 0.15 * node.diameter for c in node.child_ids if c in tree.nodes)
        if thin:
            mechs.append("THIN_CHILD_EXCESS")
            totals["THIN_CHILD_EXCESS"] += 0.03 * br.Phi_v
        if not mechs:
            mechs = ["NONE"]
        records.append(ExcessRecord(br.node_id, br.Phi_v, br.P_v, E, mechs))

    dominant = max(totals, key=totals.get, default="NONE")  # type: ignore[arg-type]
    total = sum(r.E_frak for r in records)
    return SignatureExcessAudit(
        records=records,
        total_excess=total,
        dominant=dominant if totals[dominant] > 0 else "NONE",
        messages=[f"total_E={total:.3f}, dominant={dominant}"],
    )
