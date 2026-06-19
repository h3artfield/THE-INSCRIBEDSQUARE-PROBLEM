"""Neutral escape profile classification (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.transition_escape_audit import EscapeLabel, audit_transition_escape

ProfileRoute = Literal[
    "CONCENTRATION",
    "DOMINANT_RAY",
    "POSITIVE_SCALE",
    "PLATEAU_GEOMETRY",
    "T081I_BRANCHING",
    "FINITE_CENTER",
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "REMOVABLE_COBOUNDARY",
    "COMPACT_CORE",
    "UNROUTED",
]


@dataclass
class EscapeProfileRecord:
    label: EscapeLabel
    diverging_quantity: str
    geometric_meaning: str
    removable: bool
    route: ProfileRoute


@dataclass
class NeutralEscapeProfileAudit:
    profiles: list[EscapeProfileRecord]
    all_routed: bool
    compact_core_candidate: bool
    messages: list[str]


_PROFILE_MAP: dict[EscapeLabel, tuple[str, str, ProfileRoute]] = {
    "SCALE_RATIO_ESCAPE": ("child Phi / parent Phi", "scale ratio drift", "POSITIVE_SCALE"),
    "CHILD_COUNT_ESCAPE": ("#children", "branching blow-up", "T081I_BRANCHING"),
    "CENTER_DRIFT_ESCAPE": ("center cover", "infinite-center drift", "INFINITE_CENTER"),
    "GATE_COMPLEXITY_ESCAPE": ("gate_count*diameter", "gate accumulation", "PARAMETER_DISCONNECTED"),
    "WEDGE_RESERVE_ESCAPE": ("wedge reserve", "cross-child separation", "FINITE_CENTER"),
    "RETAINED_RESERVE_ESCAPE": ("retained skeleton", "bookkeeping reserve", "REMOVABLE_COBOUNDARY"),
    "SIGN_IMBALANCE_ESCAPE": ("sign grouping", "sign cancellation pattern", "REMOVABLE_COBOUNDARY"),
    "CROSSCUT_ESCAPE": ("crosscut area", "gate chord excess", "FINITE_CENTER"),
    "BOUNDARY_RESERVE_ESCAPE": ("corona boundary", "truncation leakage", "REMOVABLE_COBOUNDARY"),
    "NORMALIZATION_DENOMINATOR_COLLAPSE": ("Phi", "zero signature node", "CONCENTRATION"),
    "NONE": ("none", "bounded coordinate", "COMPACT_CORE"),
}


def audit_neutral_escape_profiles(tree: CanonicalIntrusionTree) -> NeutralEscapeProfileAudit:
    esc = audit_transition_escape(tree)
    seen: set[EscapeLabel] = set()
    profiles: list[EscapeProfileRecord] = []
    for rec in esc.records:
        for lab in rec.escape_labels:
            if lab in seen:
                continue
            seen.add(lab)
            qty, meaning, route = _PROFILE_MAP.get(lab, ("unknown", "unknown", "UNROUTED"))
            profiles.append(
                EscapeProfileRecord(
                    lab,
                    qty,
                    meaning,
                    route in ("REMOVABLE_COBOUNDARY", "COMPACT_CORE"),
                    route if rec.route != "PENDING_ROUTE" else route,
                )
            )
    unrouted = any(p.route == "UNROUTED" for p in profiles)
    all_routed = not unrouted and bool(profiles)
    compact_candidate = all_routed and not esc.family_compact
    return NeutralEscapeProfileAudit(
        profiles=profiles,
        all_routed=all_routed,
        compact_core_candidate=compact_candidate,
        messages=[f"profiles={len(profiles)}, routed={all_routed}"],
    )
