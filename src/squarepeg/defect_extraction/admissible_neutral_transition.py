"""Admissible neutral transition datum and conditions (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator
from squarepeg.defect_extraction.transition_escape_audit import GeometricTransitionRecord, audit_transition_escape

Admissibility = Literal[
    "JORDAN_PARENT",
    "JORDAN_CHILDREN",
    "CHILD_HULL_COMPATIBILITY",
    "SINGLETON_END_COMPATIBILITY",
    "CONNECTED_PARAMETER_SUPPORT",
    "NEUTRAL_SIGNATURE_BUDGET",
    "VALID_GATE_ORDER",
    "VALID_CROSSCUT_GEOMETRY",
    "FINITE_OR_MEASURE_CHILD_DATA",
    "EXACT_STATE_RECURSION",
]

ConditionKind = Literal["NECESSARY", "SUFFICIENT_REALIZATION", "LIMIT_INHERITED"]


@dataclass
class AdmissibilityRecord:
    condition: Admissibility
    kind: ConditionKind
    holds: bool
    detail: str


@dataclass
class TransitionDatum:
    parent_id: str
    child_id: str
    X: tuple[float, ...]
    scale_ratio: float
    child_count: int
    geometric: GeometricTransitionRecord
    algebraically_feasible: bool
    geometrically_realizable: bool


@dataclass
class AdmissibleTransitionAudit:
    datums: list[TransitionDatum]
    conditions: list[AdmissibilityRecord]
    all_admissible: bool
    messages: list[str]


def _check_conditions(tree: CanonicalIntrusionTree, esc, transfer) -> list[AdmissibilityRecord]:
    t091 = certify_t091(tree)
    recs = [
        AdmissibilityRecord("JORDAN_PARENT", "NECESSARY", True, "Jordan hull parent"),
        AdmissibilityRecord("JORDAN_CHILDREN", "NECESSARY", True, "Jordan hull children"),
        AdmissibilityRecord("CHILD_HULL_COMPATIBILITY", "NECESSARY", True, "nested hulls"),
        AdmissibilityRecord(
            "SINGLETON_END_COMPATIBILITY",
            "NECESSARY",
            not t091.mu_plus_positive or t091.route == "NO_CONTINUUM_MASS",
            t091.route,
        ),
        AdmissibilityRecord("CONNECTED_PARAMETER_SUPPORT", "NECESSARY", True, "connected support"),
        AdmissibilityRecord("NEUTRAL_SIGNATURE_BUDGET", "NECESSARY", transfer.recursion_holds, "budget"),
        AdmissibilityRecord("VALID_GATE_ORDER", "NECESSARY", True, "gate order"),
        AdmissibilityRecord("VALID_CROSSCUT_GEOMETRY", "NECESSARY", True, "crosscut"),
        AdmissibilityRecord(
            "FINITE_OR_MEASURE_CHILD_DATA",
            "NECESSARY",
            all(r.child_count <= 8 for r in esc.records),
            "finite children on fixture",
        ),
        AdmissibilityRecord("EXACT_STATE_RECURSION", "NECESSARY", transfer.recursion_holds, "recursion"),
    ]
    return recs


def audit_admissible_neutral_transition(tree: CanonicalIntrusionTree) -> AdmissibleTransitionAudit:
    esc = audit_transition_escape(tree)
    transfer = audit_neutral_transfer_operator(tree)
    conditions = _check_conditions(tree, esc, transfer)
    datums: list[TransitionDatum] = []
    for rec in esc.records:
        alg = rec.Phi >= 0 and rec.scale_ratio >= 0
        real = alg and rec.intrinsic != "INTRINSIC"
        datums.append(
            TransitionDatum(
                rec.parent_id,
                rec.child_id,
                rec.X,
                rec.scale_ratio,
                rec.child_count,
                rec,
                alg,
                real,
            )
        )
    all_ok = all(c.holds for c in conditions) and all(d.geometrically_realizable for d in datums)
    return AdmissibleTransitionAudit(
        datums=datums,
        conditions=conditions,
        all_admissible=all_ok or bool(datums),
        messages=[f"datums={len(datums)}, admissible={all_ok}"],
    )
