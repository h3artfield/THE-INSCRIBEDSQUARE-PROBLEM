"""Bellman duality on compact neutral core only (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.bellman_exact_certificate import audit_bellman_exact_certificate
from squarepeg.defect_extraction.bellman_potential import audit_bellman_potential, _eval_linear
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.compact_neutral_core import audit_compact_neutral_core
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator

T098CBranch = Literal["STRICT_BELLMAN_SEPARATION", "CRITICAL_INVARIANT_FUNCTIONAL", "NOT_APPLICABLE"]
T098CStatus = Literal["CONJECTURAL_DUALITY_TARGET", "PROVED_LOCALLY"]


@dataclass
class CompactCoreBellmanAudit:
    core_only: bool
    linear_exists: bool
    eta: float
    interval_verified: bool
    branch: T098CBranch
    messages: list[str]


@dataclass
class T098CCertificate:
    status: T098CStatus
    branch: T098CBranch
    contraction: bool
    messages: list[str]


def audit_compact_core_bellman(tree: CanonicalIntrusionTree) -> CompactCoreBellmanAudit:
    core = audit_compact_neutral_core(tree)
    if not core.sequentially_compact:
        return CompactCoreBellmanAudit(
            False, False, 0.0, False, "NOT_APPLICABLE", ["compact core not established"]
        )
    bellman = audit_bellman_potential(tree)
    cert = audit_bellman_exact_certificate(tree, bellman=bellman)
    core_ids = {r.parent_id for r in core.core_records if r.in_core}
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    state_map = {s.node_id: s for s in states.states}
    a = bellman.best.coefficients if bellman.best else (1.0, 0.8, 0.5, 0.6, 0.7, 0.3, 0.4)
    if len(a) < 7:
        a = a + (0.0,) * (7 - len(a))
    eta = 0.0
    holds = False
    for pid in core_ids:
        if pid not in state_map:
            continue
        siblings = [t for t in transfer.transfers if t.parent_id == pid]
        if not siblings or any(t.child_id not in state_map for t in siblings):
            continue
        Bp = _eval_linear(state_map[pid], a)
        child_sum = sum(_eval_linear(state_map[t.child_id], a) for t in siblings)
        if Bp > 1e-12:
            eta = max(eta, 1.0 - child_sum / Bp)
            if child_sum <= 0.97 * Bp:
                holds = True
    branch: T098CBranch = "STRICT_BELLMAN_SEPARATION" if holds and cert.any_verified else "CRITICAL_INVARIANT_FUNCTIONAL"
    return CompactCoreBellmanAudit(
        True,
        bellman.linear_exists,
        eta,
        cert.any_verified,
        branch,
        [f"eta={eta:.3f}, holds={holds}"],
    )


def certify_t098c(tree: CanonicalIntrusionTree) -> T098CCertificate:
    audit = audit_compact_core_bellman(tree)
    if audit.branch == "NOT_APPLICABLE":
        return T098CCertificate("CONJECTURAL_DUALITY_TARGET", "NOT_APPLICABLE", False, audit.messages)
    status: T098CStatus = "PROVED_LOCALLY" if audit.interval_verified and audit.branch == "STRICT_BELLMAN_SEPARATION" else "CONJECTURAL_DUALITY_TARGET"
    return T098CCertificate(status, audit.branch, audit.branch == "STRICT_BELLMAN_SEPARATION", audit.messages)
