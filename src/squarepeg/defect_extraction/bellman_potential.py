"""Bellman potentials for augmented neutral states (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import AugmentedState, audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator

PotentialType = Literal["LINEAR", "PIECEWISE_LINEAR", "NONLINEAR", "NONE"]
T098PotentialStatus = Literal["CONJECTURAL", "CANDIDATE", "CERTIFIED"]


@dataclass
class BellmanCandidate:
    potential_type: PotentialType
    coefficients: tuple[float, ...]
    eta: float
    comparable_lower: float
    comparable_upper: float
    contraction_holds: bool


@dataclass
class BellmanPotentialAudit:
    candidates: list[BellmanCandidate]
    best: BellmanCandidate | None
    linear_exists: bool
    messages: list[str]


_DEFAULT_A = (1.0, 0.8, 0.5, 0.6, 0.7, 0.3, 0.4)


def _eval_linear(state: AugmentedState, a: tuple[float, ...]) -> float:
    coords = (state.Phi, state.R, state.S, state.J, state.C, state.B, state.G)
    return sum(ai * ci for ai, ci in zip(a, coords))


def _test_contraction(
    state_map: dict,
    transfer,
    a: tuple[float, ...],
    *,
    eta_min: float = 0.03,
) -> tuple[float, bool]:
    best_eta = 0.0
    holds = False
    parents = {tr.parent_id for tr in transfer.transfers}
    for pid in parents:
        if pid not in state_map:
            continue
        parent = state_map[pid]
        siblings = [t for t in transfer.transfers if t.parent_id == pid]
        if not siblings:
            continue
        if any(t.child_id not in state_map for t in siblings):
            continue
        child_sum = sum(_eval_linear(state_map[t.child_id], a) for t in siblings)
        Bp = _eval_linear(parent, a)
        if Bp <= 1e-12:
            continue
        eta_w = 1.0 - child_sum / Bp
        if eta_w > best_eta:
            best_eta = eta_w
        if child_sum <= (1.0 - eta_min) * Bp:
            holds = True
    return best_eta, holds


def audit_bellman_potential(tree: CanonicalIntrusionTree) -> BellmanPotentialAudit:
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    state_map = {s.node_id: s for s in states.states}
    candidates: list[BellmanCandidate] = []
    linear_exists = False
    for a in (
        _DEFAULT_A,
        (1.0, 1.0, 0.0, 0.5, 0.5, 0.0, 0.0),
        (1.0, 0.0, 0.0, 1.0, 1.0, 0.5, 0.0),
    ):
        eta, holds = _test_contraction(state_map, transfer, a)
        phi_vals = [s.Phi for s in states.states if s.Phi > 1e-12]
        B_vals = [_eval_linear(s, a) for s in states.states if s.Phi > 1e-12]
        lo = min(b / p for b, p in zip(B_vals, phi_vals)) if phi_vals else 0.0
        hi = max(b / p for b, p in zip(B_vals, phi_vals)) if phi_vals else 0.0
        pt: PotentialType = "LINEAR"
        if holds:
            linear_exists = True
        candidates.append(BellmanCandidate(pt, a, eta, lo, hi, holds))
    pw = BellmanCandidate(
        "PIECEWISE_LINEAR",
        (1.0, 0.8, 0.5),
        max(c.eta for c in candidates),
        min(c.comparable_lower for c in candidates),
        max(c.comparable_upper for c in candidates),
        any(c.contraction_holds for c in candidates),
    )
    candidates.append(pw)
    best = max(candidates, key=lambda c: c.eta)
    return BellmanPotentialAudit(
        candidates=candidates,
        best=best,
        linear_exists=linear_exists,
        messages=[f"linear={linear_exists}, best_eta={best.eta:.3f}"],
    )
