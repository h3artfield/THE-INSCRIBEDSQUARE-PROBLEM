"""T105 — Measure-valued transition weak-limit closure (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.measure_admissible_transition import audit_measure_admissible_transition
from squarepeg.defect_extraction.measure_transition_tightness import audit_measure_transition_tightness

ClosureStatus = Literal[
    "WEAKLY_CONTINUOUS",
    "LOWER_SEMICONTINUOUS",
    "REQUIRES_UNIFORM_INTEGRABILITY",
    "REQUIRES_AUXILIARY_MEASURE",
    "NOT_CLOSED",
]

T105Status = Literal["CONJECTURAL_MEASURE_CLOSURE_TARGET", "PROVED_LOCALLY"]


@dataclass
class ComponentClosureRecord:
    component: str
    status: ClosureStatus


@dataclass
class MeasureTransitionClosureAudit:
    component_closure: list[ComponentClosureRecord]
    sequentially_compact: bool
    recursion_closed: bool
    messages: list[str]


@dataclass
class T105Certificate:
    status: T105Status
    closure_holds: bool
    messages: list[str]


_COMPONENTS = [
    ("Phi", "WEAKLY_CONTINUOUS"),
    ("child_measure", "REQUIRES_UNIFORM_INTEGRABILITY"),
    ("wedge_integral", "REQUIRES_AUXILIARY_MEASURE"),
    ("retained", "LOWER_SEMICONTINUOUS"),
    ("sign_group", "REQUIRES_AUXILIARY_MEASURE"),
    ("gate_order", "NOT_CLOSED"),
]


def audit_measure_transition_closure(tree: CanonicalIntrusionTree) -> MeasureTransitionClosureAudit:
    adm = audit_measure_admissible_transition(tree)
    tight = audit_measure_transition_tightness(tree)
    closed = tight.all_tight and adm.admissible
    return MeasureTransitionClosureAudit(
        component_closure=[ComponentClosureRecord(c, s) for c, s in _COMPONENTS],  # type: ignore[arg-type]
        sequentially_compact=closed,
        recursion_closed=closed and all(s != "NOT_CLOSED" for _, s in _COMPONENTS),
        messages=[f"compact={closed}"],
    )


def certify_t105(tree: CanonicalIntrusionTree) -> T105Certificate:
    audit = audit_measure_transition_closure(tree)
    status: T105Status = "PROVED_LOCALLY" if audit.sequentially_compact and audit.recursion_closed else "CONJECTURAL_MEASURE_CLOSURE_TARGET"
    return T105Certificate(status, audit.recursion_closed, audit.messages)
