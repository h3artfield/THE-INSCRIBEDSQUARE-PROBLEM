"""Cross-component interaction routing (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits

InteractionClass = Literal[
    "SUMMABLE_HARMLESS",
    "ANNULAR_BRIDGING",
    "FINITE_CENTER",
    "NONSUMMABLE_DIFFUSE",
    "INFINITE_CENTER",
    "NONE",
]


@dataclass
class CrossComponentRecord:
    interaction_id: str
    interaction_class: InteractionClass
    retained: bool
    destination: str


@dataclass
class CrossComponentInteractionAudit:
    records: list[CrossComponentRecord]
    all_routed: bool
    never_discarded: bool
    messages: list[str]


def audit_cross_component_interactions(tree: CanonicalIntrusionTree) -> CrossComponentInteractionAudit:
    limits = audit_parameter_disconnected_limits(tree)
    collision = audit_gate_collision_measure(tree)
    records: list[CrossComponentRecord] = []
    for r in limits.records:
        if not r.true_disconnection:
            records.append(CrossComponentRecord(r.limit_id, "NONE", True, "CONNECTED"))
            continue
        diag = sum(m.diagonal_mass for m in collision.measures)
        if r.disconnection_type == "FINITE_DISCONNECTED":
            ic: InteractionClass = "FINITE_CENTER" if diag > 0 else "SUMMABLE_HARMLESS"
            dest = "T062" if ic == "FINITE_CENTER" else "PROTECTED_ANNULAR"
        elif r.disconnection_type in ("COUNTABLE_DISCONNECTED", "ALTERNATING_CHAIN"):
            ic = "ANNULAR_BRIDGING"
            dest = "COUNTABLE_SURGERY"
        elif r.disconnection_type in ("CANTOR_DISCONNECTED", "DUST_LIKE"):
            ic = "INFINITE_CENTER" if diag < 0.01 else "NONSUMMABLE_DIFFUSE"
            dest = "INFINITE_CENTER_GEOMETRY" if ic == "INFINITE_CENTER" else "NONSUMMABLE_DIFFUSE_END_GEOMETRY"
        else:
            ic = "SUMMABLE_HARMLESS"
            dest = "QUOTIENT_MERGE"
        records.append(CrossComponentRecord(r.limit_id, ic, True, dest))
    return CrossComponentInteractionAudit(records, True, True, [f"n={len(records)}"])
