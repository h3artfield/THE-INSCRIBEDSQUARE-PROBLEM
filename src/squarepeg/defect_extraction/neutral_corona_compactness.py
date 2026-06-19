"""Neutral corona compactness and tangent extraction (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.normalized_end_tangent import normalize_bad_cylinder
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

NeutralLimitClass = Literal[
    "HOMOGENEOUS",
    "PERIODIC",
    "FINITE_TYPE",
    "INFINITE_CENTER",
    "COMPACTNESS_FAILURE",
]


@dataclass
class NeutralTangentRecord:
    corona_id: int
    root_id: str
    depth: int
    limit_class: NeutralLimitClass
    compact: bool
    mass_ratio_stable: bool


@dataclass
class NeutralCoronaCompactnessAudit:
    tangents: list[NeutralTangentRecord]
    compactness_holds: bool
    long_corona_exists: bool
    messages: list[str]


def audit_neutral_corona_compactness(tree: CanonicalIntrusionTree) -> NeutralCoronaCompactnessAudit:
    corona = audit_cantor_corona(tree)
    tangents: list[NeutralTangentRecord] = []
    compact_all = True
    long_corona = any(c.depth >= 2 for c in corona.coronas)

    for c in corona.coronas:
        root_rec = cylinder_density(tree, c.root_id)
        try:
            renorm = normalize_bad_cylinder(tree, c.root_id)
            ratios = [n.mu_tilde / n.phi_tilde if n.phi_tilde > 1e-9 else 0.0 for n in renorm.nodes[:5]]
            stable = max(ratios, default=0) - min(ratios, default=0) < 0.3 if ratios else True
            limit: NeutralLimitClass = "HOMOGENEOUS" if stable else "FINITE_TYPE"
            compact = True
        except Exception:
            stable = False
            limit = "COMPACTNESS_FAILURE"
            compact = False
            compact_all = False
        tangents.append(
            NeutralTangentRecord(c.corona_id, c.root_id, c.depth, limit, compact, stable)
        )

    return NeutralCoronaCompactnessAudit(
        tangents=tangents,
        compactness_holds=compact_all and bool(tangents),
        long_corona_exists=long_corona,
        messages=[f"tangents={len(tangents)}, compact={compact_all}, long={long_corona}"],
    )
