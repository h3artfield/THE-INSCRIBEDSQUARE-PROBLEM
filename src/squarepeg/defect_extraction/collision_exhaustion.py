"""Collision classification and exhaustion (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure

ExhaustionClass = Literal[
    "HARMLESS_MULTIPLICITY",
    "CONCENTRATED_COLLISION",
    "PARAMETER_MERGER",
    "SHARED_GATE_CLUSTER",
    "PINCHED_HULL",
    "NON_JORDAN_COLLISION",
    "NONE",
]


@dataclass
class CollisionExhaustionRecord:
    parent_id: str
    diagonal_mass: float
    exhaustion_class: ExhaustionClass
    routed: bool


@dataclass
class CollisionExhaustionAudit:
    records: list[CollisionExhaustionRecord]
    all_classified: bool
    harmless_quotient_ok: bool
    messages: list[str]


_CLASS_MAP = {
    "HARMLESS_DUPLICATE_GATE": "HARMLESS_MULTIPLICITY",
    "RANK_MULTIPLICITY_COLLISION": "CONCENTRATED_COLLISION",
    "PARAMETER_COMPONENT_MERGER": "PARAMETER_MERGER",
    "SHARED_GATE_DEGENERATION": "SHARED_GATE_CLUSTER",
    "PINCHED_HULL_COLLISION": "PINCHED_HULL",
    "NON_JORDAN_COLLISION": "NON_JORDAN_COLLISION",
    "NONE": "NONE",
}


def audit_collision_exhaustion(tree: CanonicalIntrusionTree) -> CollisionExhaustionAudit:
    lam = audit_gate_collision_measure(tree)
    records: list[CollisionExhaustionRecord] = []
    harmless_ok = True
    for m in lam.measures:
        if not m.atoms:
            records.append(CollisionExhaustionRecord(m.parent_id, m.diagonal_mass, "NONE", True))
            continue
        for a in m.atoms:
            ec: ExhaustionClass = _CLASS_MAP.get(a.collision_class, "NON_JORDAN_COLLISION")  # type: ignore[arg-type]
            routed = a.route != "NONE" or ec == "NONE"
            if ec == "HARMLESS_MULTIPLICITY" and a.route != "QUOTIENT_MERGE":
                harmless_ok = False
            records.append(CollisionExhaustionRecord(m.parent_id, m.diagonal_mass, ec, routed))
    all_c = all(r.routed for r in records)
    return CollisionExhaustionAudit(
        records=records,
        all_classified=all_c or not records,
        harmless_quotient_ok=harmless_ok,
        messages=[f"n={len(records)}"],
    )
