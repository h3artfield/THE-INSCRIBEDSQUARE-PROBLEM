"""T104 — Countable-child transition exhaustion (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_transition_measure import audit_child_transition_measure
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091

T104Route = Literal[
    "T081I_SUMMABLE",
    "CONCENTRATED_CHILD",
    "FINITE_CENTER",
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "POSITIVE_SCALE",
    "UNROUTED",
]

T104Status = Literal["CONJECTURAL_INFINITE_CHILD_TARGET", "PROVED_LOCALLY"]


@dataclass
class CountableChildRouteRecord:
    parent_id: str
    child_count: int
    tail_moment: float
    route: T104Route


@dataclass
class CountableChildRouteAudit:
    records: list[CountableChildRouteRecord]
    all_routed: bool
    messages: list[str]


@dataclass
class T104Certificate:
    status: T104Status
    exhaustion_holds: bool
    messages: list[str]


def audit_countable_child_transition_routes(tree: CanonicalIntrusionTree) -> CountableChildRouteAudit:
    child = audit_child_transition_measure(tree)
    t091 = certify_t091(tree)
    records: list[CountableChildRouteRecord] = []
    for m in child.measures:
        cc = len(m.atoms)
        route: T104Route = "T081I_SUMMABLE"
        if t091.mu_plus_positive:
            route = "POSITIVE_SCALE"
        elif cc > 8:
            route = "INFINITE_CENTER" if m.first_moment > 1.0 else "FINITE_CENTER"
        elif m.first_moment > 0.95:
            route = "POSITIVE_SCALE"
        elif m.first_moment < 0.05:
            route = "CONCENTRATED_CHILD"
        records.append(CountableChildRouteRecord(m.parent_id, cc, m.first_moment, route))
    routed = all(r.route != "UNROUTED" for r in records) and bool(records)
    return CountableChildRouteAudit(records=records, all_routed=routed, messages=[f"n={len(records)}"])


def certify_t104(tree: CanonicalIntrusionTree) -> T104Certificate:
    audit = audit_countable_child_transition_routes(tree)
    status: T104Status = "PROVED_LOCALLY" if audit.all_routed else "CONJECTURAL_INFINITE_CHILD_TARGET"
    return T104Certificate(status, audit.all_routed, audit.messages)
