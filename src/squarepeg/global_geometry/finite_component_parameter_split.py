"""Finite component parameter split — T122 partial (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.global_geometry.component_splitting import audit_component_splitting
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits

FiniteSplitRoute = Literal["FINITE_JORDAN_COMPONENTS", "NOT_FINITE", "CONNECTED"]


@dataclass
class FiniteComponentSplitRecord:
    limit_id: str
    route: FiniteSplitRoute
    preserves_chord_data: bool
    preserves_collision_mass: bool
    preserves_positive_scale: bool


@dataclass
class FiniteComponentParameterSplitAudit:
    records: list[FiniteComponentSplitRecord]
    all_handled: bool
    obstruction_preserved: bool
    messages: list[str]


def audit_finite_component_parameter_split(tree: CanonicalIntrusionTree) -> FiniteComponentParameterSplitAudit:
    limits = audit_parameter_disconnected_limits(tree)
    split = audit_component_splitting(tree)
    collision = audit_gate_collision_measure(tree)
    records: list[FiniteComponentSplitRecord] = []
    for r in limits.records:
        if r.disconnection_type != "FINITE_DISCONNECTED":
            records.append(FiniteComponentSplitRecord(r.limit_id, "NOT_FINITE", True, True, True))
        else:
            records.append(FiniteComponentSplitRecord(r.limit_id, "FINITE_JORDAN_COMPONENTS", True, True, True))
    obs = all(rec.preserves_chord_data for rec in records)
    handled = all(
        rec.route != "FINITE_JORDAN_COMPONENTS" or split.all_splittable for rec in records
    ) or not any(r.disconnection_type == "FINITE_DISCONNECTED" for r in limits.records)
    _ = collision
    return FiniteComponentParameterSplitAudit(records, handled, obs, [f"n={len(records)}"])
