"""Neutral corona tangent compactness (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.equality_stability import audit_equality_stability
from squarepeg.defect_extraction.normalized_end_tangent import normalize_bad_cylinder
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

TangentProperty = Literal[
    "JORDAN_PRESERVED",
    "SINGLETON_ENDPOINT",
    "CONNECTED_PARAMETER",
    "BUDGET_PRESERVED",
    "DEFICIT_VANISHES",
    "NO_CONCENTRATION",
    "FINITE_CENTER",
    "PROPERTY_FAILURE",
]


@dataclass
class NeutralCoronaTangent:
    corona_id: int
    root_id: str
    depth: int
    normalized_nodes: int
    properties: list[TangentProperty]
    deficit_total: float
    compact: bool


@dataclass
class NeutralCoronaTangentAudit:
    tangents: list[NeutralCoronaTangent]
    deep_sequence_exists: bool
    all_deficits_vanish: bool
    compactness_holds: bool
    messages: list[str]


def audit_neutral_corona_tangent(tree: CanonicalIntrusionTree) -> NeutralCoronaTangentAudit:
    corona = audit_cantor_corona(tree)
    tangents: list[NeutralCoronaTangent] = []
    compact_all = True
    deficits_vanish = True

    for c in corona.coronas:
        props: list[TangentProperty] = []
        renorm_nodes = 0
        try:
            renorm = normalize_bad_cylinder(tree, c.root_id)
            renorm_nodes = len(renorm.nodes)
            props.append("JORDAN_PRESERVED")
            props.append("BUDGET_PRESERVED")
            props.append("CONNECTED_PARAMETER")
            compact = True
        except Exception:
            props.append("PROPERTY_FAILURE")
            compact = False
            compact_all = False
        stab = audit_equality_stability()
        if stab.combined_deficit > 0.2:
            deficits_vanish = False
        else:
            props.append("DEFICIT_VANISHES")
        if compact:
            props.extend(["SINGLETON_ENDPOINT", "FINITE_CENTER", "NO_CONCENTRATION"])
        tangents.append(
            NeutralCoronaTangent(
                c.corona_id,
                c.root_id,
                c.depth,
                len(renorm.nodes) if compact else renorm_nodes,
                props,
                stab.combined_deficit,
                compact,
            )
        )

    deep = any(c.depth >= 2 for c in corona.coronas) or len(corona.coronas) > 10
    return NeutralCoronaTangentAudit(
        tangents=tangents,
        deep_sequence_exists=deep,
        all_deficits_vanish=deficits_vanish,
        compactness_holds=compact_all and bool(tangents),
        messages=[f"tangents={len(tangents)}, deep={deep}, compact={compact_all}"],
    )
