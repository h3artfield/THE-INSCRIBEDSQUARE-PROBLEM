"""Compact-core occupation measures and balance (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.compact_neutral_core import audit_compact_neutral_core
from squarepeg.defect_extraction.compact_core_bellman import audit_compact_core_bellman
from squarepeg.defect_extraction.measure_valued_transition import audit_measure_valued_transition
from squarepeg.defect_extraction.neutral_occupation_measure import audit_neutral_occupation_measure


@dataclass
class CompactCoreOccupationAudit:
    boundary_leakage_negligible: bool
    balance_holds: bool
    zero_slack_ae: bool
    total_mass: float
    messages: list[str]


def audit_compact_core_occupation(tree: CanonicalIntrusionTree) -> CompactCoreOccupationAudit:
    core = audit_compact_neutral_core(tree)
    occ = audit_neutral_occupation_measure(tree)
    measure = audit_measure_valued_transition(tree)
    bellman = audit_compact_core_bellman(tree)
    states = audit_augmented_neutral_state(tree)
    boundary_ok = occ.measure.boundary_leakage < 0.2
    balance = core.sequentially_compact and measure.all_tight
    slack_ok = bellman.branch != "STRICT_BELLMAN_SEPARATION" or bellman.eta < 0.05
    return CompactCoreOccupationAudit(
        boundary_leakage_negligible=boundary_ok,
        balance_holds=balance,
        zero_slack_ae=slack_ok,
        total_mass=occ.measure.total_mass,
        messages=[f"boundary={boundary_ok}, balance={balance}"],
    )
