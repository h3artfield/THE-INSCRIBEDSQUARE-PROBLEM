"""Compact neutral transition core (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.measure_valued_transition import audit_measure_valued_transition
from squarepeg.defect_extraction.neutral_escape_profiles import audit_neutral_escape_profiles
from squarepeg.defect_extraction.neutral_gauge_quotient import audit_neutral_gauge_quotient
from squarepeg.defect_extraction.projective_neutral_state import audit_projective_neutral_state
from squarepeg.defect_extraction.transition_escape_audit import audit_transition_escape

ClosureStatus = Literal[
    "CONTINUOUS",
    "LOWER_SEMICONTINUOUS",
    "MEASURE_CONTINUOUS",
    "REQUIRES_AUXILIARY_DATA",
    "NOT_CLOSED",
]


@dataclass
class CoordinateClosureRecord:
    coordinate: str
    status: ClosureStatus


@dataclass
class CompactCoreRecord:
    parent_id: str
    scale_ratio: float
    in_core: bool


@dataclass
class CompactNeutralCoreAudit:
    core_records: list[CompactCoreRecord]
    sequentially_compact: bool
    recursion_closed: bool
    coordinate_closure: list[CoordinateClosureRecord]
    core_size: int
    messages: list[str]


_COORD_CLOSURE = [
    ("Phi", "CONTINUOUS"),
    ("R", "REQUIRES_AUXILIARY_DATA"),
    ("S", "REQUIRES_AUXILIARY_DATA"),
    ("J", "LOWER_SEMICONTINUOUS"),
    ("C", "CONTINUOUS"),
    ("B", "MEASURE_CONTINUOUS"),
    ("G", "CONTINUOUS"),
]


def audit_compact_neutral_core(tree: CanonicalIntrusionTree) -> CompactNeutralCoreAudit:
    esc = audit_transition_escape(tree)
    profiles = audit_neutral_escape_profiles(tree)
    proj = audit_projective_neutral_state(tree)
    gauge = audit_neutral_gauge_quotient(tree)
    measure = audit_measure_valued_transition(tree)
    core_records: list[CompactCoreRecord] = []
    for rec in esc.records:
        if rec.intrinsic == "ROUTED_BRANCH":
            in_core = False
        elif rec.escape_labels == ["NONE"]:
            in_core = True
        else:
            in_core = False
        core_records.append(CompactCoreRecord(rec.parent_id, rec.scale_ratio, in_core))
    core_size = sum(1 for r in core_records if r.in_core)
    ratios = [r.scale_ratio for r in core_records if r.in_core]
    ratio_spread = (max(ratios) - min(ratios)) if ratios else 0.0
    seq_compact = (
        profiles.all_routed
        and proj.section_closed
        and gauge.hausdorff
        and measure.all_tight
        and ratio_spread < 0.5
        and core_size > 0
    )
    recursion_closed = seq_compact and all(c.status != "NOT_CLOSED" for c in [
        CoordinateClosureRecord(c, s) for c, s in _COORD_CLOSURE
    ])
    return CompactNeutralCoreAudit(
        core_records=core_records,
        sequentially_compact=seq_compact,
        recursion_closed=recursion_closed,
        coordinate_closure=[CoordinateClosureRecord(c, s) for c, s in _COORD_CLOSURE],
        core_size=core_size,
        messages=[f"core={core_size}, compact={seq_compact}, closed={recursion_closed}"],
    )
