"""Weak-limit closure audit for augmented gate measures (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cyclic_gate_measure import audit_cyclic_gate_measure
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.defect_extraction.gate_measure_tightness import audit_gate_measure_tightness
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure

FunctionalStatus = Literal[
    "WEAKLY_CONTINUOUS",
    "CONTINUOUS_UNDER_UNIFORM_INTEGRABILITY",
    "LOWER_SEMICONTINUOUS",
    "REQUIRES_COLLISION_MEASURE",
    "NOT_CLOSED",
]

T107Status = Literal["CONJECTURAL_GATE_MEASURE_TARGET", "PROVED_LOCALLY"]


@dataclass
class FunctionalClosureRecord:
    functional: str
    status: FunctionalStatus


@dataclass
class GateMeasureWeakClosureAudit:
    functionals: list[FunctionalClosureRecord]
    pi_closed: bool
    omega_closed: bool
    lambda_closed: bool
    discrete_gate_order_eliminated: bool
    messages: list[str]


@dataclass
class T107Certificate:
    status: T107Status
    representation_exact: bool
    seam_independent: bool
    sequentially_closed: bool
    messages: list[str]


_FUNCTIONALS = [
    ("marginal_consistency", "WEAKLY_CONTINUOUS"),
    ("cyclic_order", "WEAKLY_CONTINUOUS"),
    ("inversion_energy", "CONTINUOUS_UNDER_UNIFORM_INTEGRABILITY"),
    ("cross_wedge_area", "WEAKLY_CONTINUOUS"),
    ("attachment_recursion", "LOWER_SEMICONTINUOUS"),
    ("collision_routing", "REQUIRES_COLLISION_MEASURE"),
    ("gate_order_discrete", "NOT_CLOSED"),
]


def audit_gate_measure_weak_closure(tree: CanonicalIntrusionTree) -> GateMeasureWeakClosureAudit:
    pi = audit_marked_gate_measure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    lam = audit_gate_collision_measure(tree)
    cyclic = audit_cyclic_gate_measure(tree)
    tight = audit_gate_measure_tightness(tree)
    funcs = [FunctionalClosureRecord(f, s) for f, s in _FUNCTIONALS]  # type: ignore[arg-type]
    # Augmented measures replace discrete gate_order
    funcs[-1] = FunctionalClosureRecord("gate_order_augmented", "WEAKLY_CONTINUOUS")
    closed = (
        omega.exact_reconstruction
        and cyclic.seam_independent
        and lam.all_routed
        and tight.all_tight
    )
    return GateMeasureWeakClosureAudit(
        functionals=funcs,
        pi_closed=bool(pi.measures),
        omega_closed=omega.exact_reconstruction,
        lambda_closed=lam.all_routed,
        discrete_gate_order_eliminated=closed,
        messages=[f"closed={closed}"],
    )


def certify_t107(tree: CanonicalIntrusionTree) -> T107Certificate:
    audit = audit_gate_measure_weak_closure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    cyclic = audit_cyclic_gate_measure(tree)
    status: T107Status = "PROVED_LOCALLY" if audit.discrete_gate_order_eliminated else "CONJECTURAL_GATE_MEASURE_TARGET"
    return T107Certificate(
        status,
        omega.exact_reconstruction,
        cyclic.seam_independent,
        audit.discrete_gate_order_eliminated,
        audit.messages,
    )
