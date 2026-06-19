"""Projective normalization of augmented neutral states (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

BoundaryClass = Literal[
    "ROUTED_GEOMETRIC_BOUNDARY",
    "REMOVABLE_GAUGE_BOUNDARY",
    "GENUINE_PROJECTIVE_CRITICAL_STATE",
    "INVALID_NORMALIZATION",
    "INTERIOR",
]


@dataclass
class ProjectiveStateRecord:
    node_id: str
    X_star_norm: float
    X_bar: tuple[float, float, float, float, float, float, float]
    Phi_fraction: float
    boundary_class: BoundaryClass


@dataclass
class ProjectiveNeutralStateAudit:
    records: list[ProjectiveStateRecord]
    section_closed: bool
    coercive: bool
    messages: list[str]


def _star_norm(st) -> float:
    return st.Phi + abs(st.R) + abs(st.S) + abs(st.J) + abs(st.C) + abs(st.B) + st.G


def audit_projective_neutral_state(tree: CanonicalIntrusionTree) -> ProjectiveNeutralStateAudit:
    states = audit_augmented_neutral_state(tree)
    records: list[ProjectiveStateRecord] = []
    coercive = True
    for s in states.states:
        norm = _star_norm(s)
        if norm <= 1e-12:
            bc: BoundaryClass = "INVALID_NORMALIZATION"
            coercive = False
        else:
            frac = s.Phi / norm
            if frac < 0.05:
                bc = "GENUINE_PROJECTIVE_CRITICAL_STATE"
                coercive = False
            elif frac < 0.15:
                bc = "REMOVABLE_GAUGE_BOUNDARY"
            else:
                bc = "INTERIOR"
        inv = 1.0 / norm if norm > 1e-12 else 0.0
        X_bar = tuple(c * inv for c in (s.Phi, s.R, s.S, s.J, s.C, s.B, s.G))
        records.append(ProjectiveStateRecord(s.node_id, norm, X_bar, s.Phi / max(norm, 1e-12), bc))
    interior = sum(1 for r in records if r.boundary_class == "INTERIOR")
    closed = interior >= 0.5 * max(len(records), 1)
    return ProjectiveNeutralStateAudit(
        records=records,
        section_closed=closed,
        coercive=coercive,
        messages=[f"records={len(records)}, coercive={coercive}"],
    )
