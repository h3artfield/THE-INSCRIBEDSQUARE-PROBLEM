"""T093 coverage accounting and neutral mass tracking (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.multigeneration_packing import (
    P_L,
    _all_descendants,
    audit_multigeneration_packing,
)
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class CoverageRecord:
    node_id: str
    Phi_v: float
    Phi_desc: float
    P_L: float
    cov_L: float
    Phi_uncovered: float
    Phi_contract: float
    Phi_neutral: float
    Phi_bad: float


@dataclass
class T093CoverageAudit:
    records: list[CoverageRecord]
    measure_type: str
    total_uncovered_phi: float
    neutral_phi_fraction: float
    residual_in_neutral: bool
    messages: list[str]


def audit_t093_coverage(
    tree: CanonicalIntrusionTree,
    *,
    L: int = 2,
) -> T093CoverageAudit:
    """Coverage = P_L(v) / Phi_desc(v) in signature scale Phi_end, not end mass."""
    corona = audit_cantor_corona(tree)
    pack = audit_multigeneration_packing(tree)
    L = pack.uniform_L if pack.multigen_contraction else L
    class_map = {c.node_id: c.node_class for c in corona.classifications}
    records: list[CoverageRecord] = []
    total_uncovered = 0.0
    total_phi = 0.0
    neutral_phi = 0.0

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        phi_desc = sum(cylinder_density(tree, d).phi_v for d in _all_descendants(tree, nid))
        pl = P_L(tree, nid, L)
        cov = pl / phi_desc if phi_desc > 1e-12 else 0.0
        uncovered = max(0.0, phi_desc - pl)
        nc = class_map.get(nid, "NEUTRAL")
        phi_c = rec.phi_v if nc == "CONTRACTING" else 0.0
        phi_n = rec.phi_v if nc == "NEUTRAL" else 0.0
        phi_b = rec.phi_v if nc == "BAD" else 0.0
        records.append(
            CoverageRecord(nid, rec.phi_v, phi_desc, pl, cov, uncovered, phi_c, phi_n, phi_b)
        )
        total_uncovered += uncovered
        total_phi += rec.phi_v
        if nc == "NEUTRAL":
            neutral_phi += rec.phi_v

    return T093CoverageAudit(
        records=records,
        measure_type="SIGNATURE_SCALE_PHI_END",
        total_uncovered_phi=total_uncovered,
        neutral_phi_fraction=neutral_phi / max(total_phi, 1e-9),
        residual_in_neutral=neutral_phi > 0.3 * total_phi,
        messages=[
            f"measure=Phi_end, uncovered={total_uncovered:.3f}, neutral_frac={neutral_phi/max(total_phi,1e-9):.2f}",
        ],
    )
