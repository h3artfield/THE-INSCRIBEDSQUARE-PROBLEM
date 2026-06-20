"""Child transition measures from exact state recursion (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator
from squarepeg.defect_extraction.projective_neutral_state import _star_norm


@dataclass
class ChildStateAtom:
    child_id: str
    weight: float
    scale_ratio: float
    star_mass: float
    wedge: float


@dataclass
class ChildTransitionMeasure:
    parent_id: str
    atoms: list[ChildStateAtom]
    total_mass: float
    first_moment: float


@dataclass
class ChildTransitionMeasureAudit:
    measures: list[ChildTransitionMeasure]
    first_moment_finite: bool
    wedge_integrable: bool
    total_mass: float
    messages: list[str]


def audit_child_transition_measure(tree: CanonicalIntrusionTree) -> ChildTransitionMeasureAudit:
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    state_map = {s.node_id: s for s in states.states}
    by_parent: dict[str, list] = {}
    for tr in transfer.transfers:
        by_parent.setdefault(tr.parent_id, []).append(tr)
    measures: list[ChildTransitionMeasure] = []
    total = 0.0
    wedge_ok = True
    for pid, trs in by_parent.items():
        if pid not in state_map:
            continue
        parent = state_map[pid]
        phi_sum = sum(state_map[t.child_id].Phi for t in trs if t.child_id in state_map) or 1.0
        atoms: list[ChildStateAtom] = []
        m1 = 0.0
        mass = 0.0
        for t in trs:
            if t.child_id not in state_map:
                continue
            ch = state_map[t.child_id]
            w = ch.Phi / phi_sum
            sm = _star_norm(ch)
            wedge = abs(ch.J)
            mass += w * sm
            m1 += w * t.scale_ratio
            atoms.append(ChildStateAtom(t.child_id, w, t.scale_ratio, sm, wedge))
            if wedge > 10 * parent.Phi:
                wedge_ok = False
        total += mass
        measures.append(ChildTransitionMeasure(pid, atoms, mass, m1))
    finite = all(m.first_moment < 100 for m in measures)
    return ChildTransitionMeasureAudit(
        measures=measures,
        first_moment_finite=finite,
        wedge_integrable=wedge_ok,
        total_mass=total,
        messages=[f"measures={len(measures)}, finite={finite}"],
    )
