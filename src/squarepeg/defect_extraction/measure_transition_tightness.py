"""Coercive tightness for child transition measures (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure


@dataclass
class TightnessRecord:
    parent_id: str
    psi_moment: float
    tight: bool


@dataclass
class MeasureTransitionTightnessAudit:
    records: list[TightnessRecord]
    uniform_bound: float
    all_tight: bool
    messages: list[str]


def _psi(atom) -> float:
    return atom.star_mass + abs(atom.scale_ratio - 0.5) + atom.wedge


def audit_measure_transition_tightness(tree: CanonicalIntrusionTree) -> MeasureTransitionTightnessAudit:
    child = audit_child_transition_measure(tree)
    records: list[TightnessRecord] = []
    bound = 0.0
    for m in child.measures:
        psi = sum(a.weight * _psi(a) for a in m.atoms)
        bound = max(bound, psi)
        records.append(TightnessRecord(m.parent_id, psi, psi < 50.0))
    tight = all(r.tight for r in records) and bool(records)
    return MeasureTransitionTightnessAudit(
        records=records,
        uniform_bound=bound,
        all_tight=tight,
        messages=[f"records={len(records)}, tight={tight}"],
    )
