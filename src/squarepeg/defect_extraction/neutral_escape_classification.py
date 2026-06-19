"""T100 — Neutral transition escape classification (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.compact_neutral_core import audit_compact_neutral_core
from squarepeg.defect_extraction.neutral_escape_profiles import audit_neutral_escape_profiles
from squarepeg.defect_extraction.transition_escape_audit import audit_transition_escape

T100Branch = Literal[
    "CONCENTRATION",
    "POSITIVE_SCALE",
    "T081I",
    "FINITE_CENTER",
    "INFINITE_CENTER",
    "PARAMETER_GATE",
    "NON_JORDAN",
    "REMOVABLE_COBOUNDARY",
    "COMPACT_CORE_CONVERGENCE",
    "UNCLASSIFIED",
]

T100Status = Literal["CONJECTURAL_COMPACTNESS_TARGET", "PROVED_LOCALLY"]


@dataclass
class EscapeClassificationRecord:
    parent_id: str
    branch: T100Branch
    routed: bool


@dataclass
class NeutralEscapeClassificationAudit:
    records: list[EscapeClassificationRecord]
    all_classified: bool
    messages: list[str]


@dataclass
class T100Certificate:
    status: T100Status
    all_routed: bool
    compact_convergence_possible: bool
    messages: list[str]


def audit_neutral_escape_classification(tree: CanonicalIntrusionTree) -> NeutralEscapeClassificationAudit:
    esc = audit_transition_escape(tree)
    records: list[EscapeClassificationRecord] = []
    for rec in esc.records:
        branch: T100Branch = "UNCLASSIFIED"
        if rec.route == "POSITIVE_SCALE_END_RAY":
            branch = "POSITIVE_SCALE"
        elif rec.route == "CONCENTRATION":
            branch = "CONCENTRATION"
        elif rec.route == "T081I_COUNTABLE_BRANCHING":
            branch = "T081I"
        elif rec.intrinsic == "REMOVABLE_COBOUNDARY":
            branch = "REMOVABLE_COBOUNDARY"
        elif rec.escape_labels == ["NONE"]:
            branch = "COMPACT_CORE_CONVERGENCE"
        records.append(EscapeClassificationRecord(rec.parent_id, branch, branch != "UNCLASSIFIED"))
    all_classified = all(r.routed for r in records) and bool(records)
    return NeutralEscapeClassificationAudit(
        records=records,
        all_classified=all_classified,
        messages=[f"classified={all_classified}, n={len(records)}"],
    )


def certify_t100(tree: CanonicalIntrusionTree) -> T100Certificate:
    cls = audit_neutral_escape_classification(tree)
    profiles = audit_neutral_escape_profiles(tree)
    core = audit_compact_neutral_core(tree)
    status: T100Status = "PROVED_LOCALLY" if cls.all_classified and profiles.all_routed else "CONJECTURAL_COMPACTNESS_TARGET"
    return T100Certificate(
        status=status,
        all_routed=profiles.all_routed,
        compact_convergence_possible=core.sequentially_compact,
        messages=cls.messages,
    )
