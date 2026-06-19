"""Raw and normalized ledger deficits (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.equality_ledger import LedgerID, get_ledger
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.signature_budget import audit_signature_budget
from squarepeg.defect_extraction.signature_excess import audit_signature_excess

NormClass = Literal[
    "NORMALIZED",
    "ZERO_SIGNATURE_NODE",
    "DEGENERATE_NORMALIZATION",
    "VANISHING_GEOMETRY_EQUALITY",
    "UNCONTROLLED_SCALE_RATIO",
]


@dataclass
class RawDeficit:
    ledger_id: LedgerID
    node_id: str
    L_k: float
    R_k: float
    delta_k: float
    d_k: float
    norm_class: NormClass


@dataclass
class LedgerDeficitsAudit:
    deficits: list[RawDeficit]
    Delta: float
    coefficients: dict[LedgerID, float]
    messages: list[str]


_COEFF: dict[LedgerID, float] = {
    "WEDGE_PRODUCT": 1.0,
    "TRIANGLE_NORM": 1.0,
    "CAUCHY_SCHWARZ": 0.8,
    "CHILD_INCREMENT": 1.2,
    "HULL_DIAMETER": 0.5,
    "CROSSCUT_AREA": 1.0,
    "RETAINED_SKELETON": 1.5,
    "CENTER_PACKING": 0.7,
    "FINITE_CENTER_GROUP": 0.7,
    "SIGN_GROUPING": 1.0,
    "CORONA_TRUNCATION": 1.0,
    "MULTIGEN_PACKING": 1.3,
}


def _compute_raw_cached(tree, nid, lid, br, rec):
    phi = rec.phi_v
    if lid == "WEDGE_PRODUCT":
        return (br.wedge_child_child if br else 0.0, 0.5 * phi)
    if lid == "TRIANGLE_NORM":
        return (br.wedge_parent_child if br else 0.0, 0.15 * phi)
    if lid == "CHILD_INCREMENT":
        return (br.P_v if br else 0.0, phi)
    if lid == "RETAINED_SKELETON":
        return (br.retained_skeleton if br else 0.0, rec.m_v)
    if lid == "MULTIGEN_PACKING":
        from squarepeg.defect_extraction.multigeneration_packing import P_L

        pl = P_L(tree, nid, 2)
        return (pl, (1.0 - 0.05) * phi)
    return (0.0, phi)


def _compute_raw(tree: CanonicalIntrusionTree, nid: str, lid: LedgerID) -> tuple[float, float]:
    rec = cylinder_density(tree, nid)
    budget = audit_signature_budget(tree)
    br = next((b for b in budget.records if b.node_id == nid), None)
    return _compute_raw_cached(tree, nid, lid, br, rec)


def audit_ledger_deficits(tree: CanonicalIntrusionTree) -> LedgerDeficitsAudit:
    budget = audit_signature_budget(tree)
    budget_map = {b.node_id: b for b in budget.records}
    deficits: list[RawDeficit] = []
    total = 0.0
    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        br = budget_map.get(nid)
        for entry in get_ledger():
            L_k, R_k = _compute_raw_cached(tree, nid, entry.id, br, rec)
            delta = max(0.0, R_k - L_k) if entry.id != "MULTIGEN_PACKING" else max(0.0, L_k - R_k)
            nc: NormClass = "NORMALIZED"
            d_k = delta / rec.phi_v if rec.phi_v > 1e-12 else 0.0
            if rec.phi_v <= 1e-12:
                nc = "ZERO_SIGNATURE_NODE"
            elif delta <= 1e-9:
                nc = "VANISHING_GEOMETRY_EQUALITY"
            total += _COEFF[entry.id] * delta
            deficits.append(RawDeficit(entry.id, nid, L_k, R_k, delta, d_k, nc))
    return LedgerDeficitsAudit(
        deficits=deficits,
        Delta=total,
        coefficients=dict(_COEFF),
        messages=[f"deficits={len(deficits)}, Delta={total:.3f}"],
    )
