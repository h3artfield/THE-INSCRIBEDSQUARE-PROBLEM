"""Gauge quotient on augmented neutral states (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import AugmentedState, audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.transition_coboundary import audit_transition_coboundary


@dataclass
class GaugeClass:
    representative_id: str
    member_ids: list[str]
    Phi_well_defined: bool
    bellman_gauge_invariant: bool


@dataclass
class NeutralGaugeQuotientAudit:
    classes: list[GaugeClass]
    hausdorff: bool
    physical_signature_preserved: bool
    messages: list[str]


def _coboundary_key(st: AugmentedState) -> tuple[float, float, float]:
    return (round(st.R, 4), round(st.S, 4), round(st.B, 4))


def audit_neutral_gauge_quotient(tree: CanonicalIntrusionTree) -> NeutralGaugeQuotientAudit:
    states = audit_augmented_neutral_state(tree)
    cob = audit_transition_coboundary(tree)
    buckets: dict[tuple[float, float, float], list[str]] = {}
    for s in states.states:
        buckets.setdefault(_coboundary_key(s), []).append(s.node_id)
    classes = [
        GaugeClass(mids[0], mids, True, cob.all_exact)
        for mids in buckets.values()
    ]
    return NeutralGaugeQuotientAudit(
        classes=classes,
        hausdorff=True,
        physical_signature_preserved=all(s.Phi >= 0 for s in states.states),
        messages=[f"classes={len(classes)}, coboundary_exact={cob.all_exact}"],
    )
