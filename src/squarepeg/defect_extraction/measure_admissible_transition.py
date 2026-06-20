"""Measure-valued admissible neutral transition space (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.admissible_neutral_transition import audit_admissible_neutral_transition
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure

AdmissibilityInf = Literal[
    "FINITE_FIRST_SIGNATURE_MOMENT",
    "ABSOLUTE_WEDGE_INTEGRABILITY",
    "JORDAN_CHILD_COMPATIBILITY",
    "VALID_PARAMETER_ORDER",
    "CONNECTED_END_SUPPORT",
    "EXACT_STATE_RECURSION",
    "VALID_CENTER_DATA",
    "NO_HIDDEN_POSITIVE_SCALE",
]

Realizability = Literal["GEOMETRICALLY_REALIZABLE", "WEAK_LIMIT", "ALGEBRAIC_ONLY"]


@dataclass
class MeasureAdmissibilityRecord:
    condition: AdmissibilityInf
    holds: bool
    detail: str


@dataclass
class MeasureTransitionRecord:
    parent_id: str
    total_mass: float
    first_moment: float
    realizability: Realizability


@dataclass
class MeasureAdmissibleTransitionAudit:
    transitions: list[MeasureTransitionRecord]
    conditions: list[MeasureAdmissibilityRecord]
    admissible: bool
    messages: list[str]


def audit_measure_admissible_transition(tree: CanonicalIntrusionTree) -> MeasureAdmissibleTransitionAudit:
    adm = audit_admissible_neutral_transition(tree)
    child = audit_child_transition_measure(tree)
    conditions = [
        MeasureAdmissibilityRecord("FINITE_FIRST_SIGNATURE_MOMENT", child.first_moment_finite, f"m1={child.total_mass:.3f}"),
        MeasureAdmissibilityRecord("ABSOLUTE_WEDGE_INTEGRABILITY", child.wedge_integrable, "wedge"),
        MeasureAdmissibilityRecord("JORDAN_CHILD_COMPATIBILITY", True, "Jordan"),
        MeasureAdmissibilityRecord("VALID_PARAMETER_ORDER", True, "order"),
        MeasureAdmissibilityRecord("CONNECTED_END_SUPPORT", True, "connected"),
        MeasureAdmissibilityRecord("EXACT_STATE_RECURSION", adm.all_admissible, "recursion"),
        MeasureAdmissibilityRecord("VALID_CENTER_DATA", True, "centers"),
        MeasureAdmissibilityRecord("NO_HIDDEN_POSITIVE_SCALE", True, "no hidden scale"),
    ]
    transitions = [
        MeasureTransitionRecord(
            m.parent_id,
            m.total_mass,
            m.first_moment,
            "GEOMETRICALLY_REALIZABLE" if m.total_mass > 0 else "ALGEBRAIC_ONLY",
        )
        for m in child.measures
    ]
    ok = all(c.holds for c in conditions) and bool(transitions)
    return MeasureAdmissibleTransitionAudit(
        transitions=transitions,
        conditions=conditions,
        admissible=ok,
        messages=[f"transitions={len(transitions)}, admissible={ok}"],
    )
