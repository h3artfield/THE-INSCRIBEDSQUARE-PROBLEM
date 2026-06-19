"""Measure-valued child transitions (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator
from squarepeg.defect_extraction.projective_neutral_state import _star_norm


@dataclass
class ChildAtom:
    child_id: str
    weight: float
    star_mass: float


@dataclass
class MeasureValuedTransition:
    parent_id: str
    atoms: list[ChildAtom]
    total_star_mass: float
    tight: bool


@dataclass
class MeasureValuedTransitionAudit:
    transitions: list[MeasureValuedTransition]
    all_tight: bool
    finite_replacement_sufficient: bool
    messages: list[str]


def audit_measure_valued_transition(tree: CanonicalIntrusionTree) -> MeasureValuedTransitionAudit:
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    state_map = {s.node_id: s for s in states.states}
    by_parent: dict[str, list] = {}
    for tr in transfer.transfers:
        by_parent.setdefault(tr.parent_id, []).append(tr)
    transitions: list[MeasureValuedTransition] = []
    all_tight = True
    finite_ok = True
    for pid, trs in by_parent.items():
        if pid not in state_map:
            continue
        parent = state_map[pid]
        total_phi = sum(state_map[t.child_id].Phi for t in trs if t.child_id in state_map) or 1.0
        atoms: list[ChildAtom] = []
        star_sum = 0.0
        for t in trs:
            if t.child_id not in state_map:
                continue
            ch = state_map[t.child_id]
            w = ch.Phi / total_phi
            sm = _star_norm(ch)
            star_sum += w * sm
            atoms.append(ChildAtom(t.child_id, w, sm))
        cc = len(atoms)
        tight = star_sum < 50.0 * _star_norm(parent)
        if not tight:
            all_tight = False
        if cc > 8:
            finite_ok = False
        transitions.append(MeasureValuedTransition(pid, atoms, star_sum, tight))
    return MeasureValuedTransitionAudit(
        transitions=transitions,
        all_tight=all_tight,
        finite_replacement_sufficient=finite_ok,
        messages=[f"transitions={len(transitions)}, tight={all_tight}"],
    )
