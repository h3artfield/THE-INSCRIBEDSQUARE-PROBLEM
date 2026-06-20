"""Pair-interaction concentration and trichotomy (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure

PairBranch = Literal[
    "CONCENTRATION",
    "FINITE_CENTER",
    "DIFFUSE",
    "COLLISION_CONCENTRATION",
    "POSITIVE_SCALE",
    "SUMMABLE",
]


@dataclass
class PairInteractionRecord:
    parent_id: str
    wedge_mass: float
    branch: PairBranch
    routed: bool


@dataclass
class PairInteractionConcentrationAudit:
    records: list[PairInteractionRecord]
    all_routed: bool
    diffuse_routed: bool
    messages: list[str]


def audit_pair_interaction_concentration(tree: CanonicalIntrusionTree) -> PairInteractionConcentrationAudit:
    omega = audit_gate_pair_interaction_measure(tree)
    t091 = certify_t091(tree)
    records: list[PairInteractionRecord] = []
    diffuse_ok = True
    for m in omega.measures:
        mass = sum(abs(p.wedge) for p in m.pairs)
        branch: PairBranch = "SUMMABLE"
        if t091.mu_plus_positive:
            branch = "POSITIVE_SCALE"
        elif mass > 1.0:
            branch = "CONCENTRATION"
        elif mass > 0.3:
            branch = "FINITE_CENTER"
        elif mass > 0.05:
            branch = "DIFFUSE"
        elif mass > 0.0:
            branch = "SUMMABLE"
        routed = branch != "DIFFUSE" or t091.mu_plus_positive or mass < 0.2
        if branch == "DIFFUSE" and not routed:
            diffuse_ok = False
        records.append(PairInteractionRecord(m.parent_id, mass, branch, routed))
    all_r = all(r.routed for r in records) and bool(records)
    return PairInteractionConcentrationAudit(
        records=records,
        all_routed=all_r or t091.mu_plus_positive,
        diffuse_routed=diffuse_ok or t091.mu_plus_positive,
        messages=[f"n={len(records)}"],
    )
