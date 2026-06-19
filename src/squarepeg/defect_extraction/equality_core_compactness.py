"""Equality-core tangent compactness (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.normalized_end_tangent import normalize_bad_cylinder
from squarepeg.defect_extraction.tree_core_selection import audit_tree_core_selection

CoreCompactness = Literal["COMPACT", "NOT_CLOSED", "PARTIAL"]


@dataclass
class EqualityCoreTangent:
    core_root: str
    normalized_nodes: int
    omitted_signature: float
    compactness: CoreCompactness
    all_deficits_vanish: bool


@dataclass
class EqualityCoreCompactnessAudit:
    tangents: list[EqualityCoreTangent]
    compactness_holds: bool
    messages: list[str]


def audit_equality_core_compactness(tree: CanonicalIntrusionTree) -> EqualityCoreCompactnessAudit:
    cores = audit_tree_core_selection(tree)
    tangents: list[EqualityCoreTangent] = []
    compact_all = True
    for c in cores.cores:
        if not c.coherent:
            continue
        try:
            renorm = normalize_bad_cylinder(tree, c.root_id)
            compact: CoreCompactness = "COMPACT"
            vanish = c.max_deficit < 0.15
        except Exception:
            renorm = None
            compact = "NOT_CLOSED"
            vanish = False
            compact_all = False
        tangents.append(
            EqualityCoreTangent(
                c.root_id,
                len(renorm.nodes) if renorm else 0,
                1.0 - c.signature_coverage,
                compact,
                vanish,
            )
        )
    return EqualityCoreCompactnessAudit(
        tangents=tangents,
        compactness_holds=compact_all and bool(tangents),
        messages=[f"tangents={len(tangents)}, compact={compact_all}"],
    )
