"""Diagonal gate collision measure Lambda_v (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure

CollisionClass = Literal[
    "HARMLESS_DUPLICATE_GATE",
    "RANK_MULTIPLICITY_COLLISION",
    "SHARED_GATE_DEGENERATION",
    "PARAMETER_COMPONENT_MERGER",
    "PINCHED_HULL_COLLISION",
    "NON_JORDAN_COLLISION",
    "NONE",
]


@dataclass
class CollisionAtom:
    parent_id: str
    gate_i: int
    gate_j: int
    mass: float
    collision_class: CollisionClass
    route: str


@dataclass
class GateCollisionMeasure:
    parent_id: str
    atoms: list[CollisionAtom]
    diagonal_mass: float


@dataclass
class GateCollisionAudit:
    measures: list[GateCollisionMeasure]
    all_routed: bool
    messages: list[str]


def audit_gate_collision_measure(tree: CanonicalIntrusionTree) -> GateCollisionAudit:
    marked = audit_marked_gate_measure(tree)
    measures: list[GateCollisionMeasure] = []
    for m in marked.measures:
        atoms: list[CollisionAtom] = []
        diag = 0.0
        seen: set[tuple[float, float]] = set()
        for i, a in enumerate(m.atoms):
            key = (round(a.boundary_phase, 4), round(a.parameter_phase, 4))
            cc: CollisionClass = "NONE"
            route = "NONE"
            if key in seen:
                cc = "HARMLESS_DUPLICATE_GATE"
                route = "QUOTIENT_MERGE"
                diag += a.attachment
            seen.add(key)
            if cc != "NONE":
                atoms.append(CollisionAtom(m.parent_id, i, i, a.attachment, cc, route))
        measures.append(GateCollisionMeasure(m.parent_id, atoms, diag))
    routed = all(
        all(a.route != "NONE" or a.collision_class == "NONE" for a in gm.atoms)
        for gm in measures
    )
    return GateCollisionAudit(
        measures=measures,
        all_routed=routed,
        messages=[f"measures={len(measures)}"],
    )
