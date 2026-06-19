"""Invariant state measures and master Bellman slack (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.bellman_potential import audit_bellman_potential, _eval_linear
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_occupation_measure import audit_neutral_occupation_measure
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator


@dataclass
class InvariantStateMeasure:
    stationary: bool
    average_slack: float
    zero_slack_fraction: float
    boundary_vanishes: bool


@dataclass
class InvariantStateAudit:
    measure: InvariantStateMeasure
    balance_holds: bool
    messages: list[str]


def audit_invariant_state_measure(tree: CanonicalIntrusionTree) -> InvariantStateAudit:
    occ = audit_neutral_occupation_measure(tree)
    bellman = audit_bellman_potential(tree)
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    state_map = {s.node_id: s for s in states.states}
    a = bellman.best.coefficients if bellman.best else (1.0, 0.8, 0.5, 0.6, 0.7, 0.3, 0.4)
    if len(a) < 7:
        a = a + (0.0,) * (7 - len(a))
    slack_vals: list[float] = []
    for tr in transfer.transfers:
        if tr.parent_id not in state_map:
            continue
        parent = state_map[tr.parent_id]
        siblings = [t for t in transfer.transfers if t.parent_id == tr.parent_id]
        child_sum = sum(
            _eval_linear(state_map[t.child_id], a)
            for t in siblings
            if t.child_id in state_map
        )
        Bp = _eval_linear(parent, a)
        slack_vals.append(Bp - child_sum)
    avg_slack = sum(slack_vals) / max(len(slack_vals), 1)
    zero_frac = sum(1 for s in slack_vals if abs(s) < 0.01 * max(abs(avg_slack), 1e-9)) / max(len(slack_vals), 1)
    stationary = abs(avg_slack) < 0.05 * max(
        (_eval_linear(s, a) for s in states.states),
        default=1.0,
    )
    boundary_ok = occ.measure.boundary_leakage < 0.15
    return InvariantStateAudit(
        measure=InvariantStateMeasure(stationary, avg_slack, zero_frac, boundary_ok),
        balance_holds=stationary and boundary_ok,
        messages=[f"avg_slack={avg_slack:.3f}, stationary={stationary}"],
    )
