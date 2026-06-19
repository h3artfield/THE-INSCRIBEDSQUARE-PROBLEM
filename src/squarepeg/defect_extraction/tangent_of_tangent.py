"""Tangent-of-tangent analysis (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_density_process import audit_end_density_process
from squarepeg.defect_extraction.normalized_end_tangent import normalize_bad_cylinder
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density, cylinder_density

TangentLimitClass = Literal[
    "HOMOGENEOUS",
    "PERIODIC",
    "FINITE_TYPE",
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "COMPACTNESS_FAILURE",
]


@dataclass
class TangentOfTangentRecord:
    base_node: str
    D_before: float
    D_after: float
    compact: bool
    limit_class: TangentLimitClass


@dataclass
class TangentOfTangentAudit:
    records: list[TangentOfTangentRecord]
    compactness_holds: bool
    homogeneous_carleson: bool
    messages: list[str]


def _bad_cylinders(tree: CanonicalIntrusionTree, *, eta: float = 0.35) -> list[str]:
    out: list[str] = []
    for nid in tree.nodes:
        rec = cylinder_density(tree, nid)
        if rec.phi_v > 1e-12 and rec.D_v >= eta:
            out.append(nid)
    return out[:8]


def audit_tangent_of_tangent(tree: CanonicalIntrusionTree) -> TangentOfTangentAudit:
    nc = audit_noncarleson_end_density(tree)
    proc = audit_end_density_process(tree)
    records: list[TangentOfTangentRecord] = []
    compact_all = True
    hom_carleson = True

    for nid in _bad_cylinders(tree):
        before = cylinder_density(tree, nid)
        try:
            renorm = normalize_bad_cylinder(tree, nid)
        except Exception:
            records.append(
                TangentOfTangentRecord(nid, before.D_v, before.D_v, False, "COMPACTNESS_FAILURE")
            )
            compact_all = False
            continue
        after_D = renorm.nodes[0].D_tilde * before.D_v if renorm.nodes else before.D_v
        D_ratio = after_D / before.D_v if before.D_v > 1e-9 else 1.0
        limit: TangentLimitClass = "HOMOGENEOUS"
        if abs(D_ratio - 1.0) < 0.15:
            limit = "HOMOGENEOUS"
        elif abs(D_ratio - 0.5) < 0.15:
            limit = "PERIODIC"
        elif after_D > before.D_v * 1.5:
            limit = "INFINITE_CENTER"
            hom_carleson = False
        elif not all(n.jordan_hull for n in renorm.nodes):
            limit = "NON_JORDAN"
            hom_carleson = False
        else:
            limit = "FINITE_TYPE"

        compact = limit not in ("COMPACTNESS_FAILURE", "INFINITE_CENTER")
        if not compact:
            compact_all = False
        records.append(TangentOfTangentRecord(nid, before.D_v, after_D, compact, limit))

    return TangentOfTangentAudit(
        records=records,
        compactness_holds=compact_all and bool(records),
        homogeneous_carleson=hom_carleson and proc.D_limsup < 2.0,
        messages=[f"records={len(records)}, compact={compact_all}"],
    )
