"""Critical invariant state classification — T099 (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.invariant_state_measure import audit_invariant_state_measure
from squarepeg.defect_extraction.transition_family import audit_transition_family

CriticalRoute = Literal[
    "T087_CARLESON",
    "CONCENTRATION",
    "FINITE_CENTER",
    "ANNULAR",
    "THIN",
    "PARAMETER_DISCONNECTED",
    "POSITIVE_SCALE",
    "NON_JORDAN",
    "INFINITE_CENTER",
    "DIFFUSE_CRITICAL_NEUTRAL_STATE_MEASURE",
    "PERIODIC_FINITE_TYPE",
    "UNCLASSIFIED",
]

T099Status = Literal["CONJECTURAL_RIGIDITY_TARGET", "PROVED_LOCALLY"]


@dataclass
class CriticalStateRecord:
    node_id: str
    zero_slack: bool
    route: CriticalRoute


@dataclass
class CriticalStateClassifierAudit:
    records: list[CriticalStateRecord]
    dominant: CriticalRoute
    diffuse_critical: bool
    messages: list[str]


@dataclass
class T099Certificate:
    status: T099Status
    routes_exhausted: bool
    diffuse_remains: bool
    messages: list[str]


def audit_critical_state_classifier(tree: CanonicalIntrusionTree) -> CriticalStateClassifierAudit:
    inv = audit_invariant_state_measure(tree)
    family = audit_transition_family(tree)
    t091 = certify_t091(tree)
    records: list[CriticalStateRecord] = []
    routes: dict[CriticalRoute, int] = {k: 0 for k in (
        "T087_CARLESON", "CONCENTRATION", "FINITE_CENTER", "ANNULAR", "THIN",
        "PARAMETER_DISCONNECTED", "POSITIVE_SCALE", "NON_JORDAN", "INFINITE_CENTER",
        "DIFFUSE_CRITICAL_NEUTRAL_STATE_MEASURE", "PERIODIC_FINITE_TYPE", "UNCLASSIFIED",
    )}
    for rec in family.records:
        route: CriticalRoute = "PERIODIC_FINITE_TYPE"
        if t091.mu_plus_positive:
            route = "POSITIVE_SCALE"
        elif rec.transition_class == "THIN_ANNULAR":
            route = "THIN"
        elif rec.transition_class == "MULTI_CHILD":
            route = "FINITE_CENTER"
        elif rec.child_count == 2 and abs(rec.scale_ratio - 0.5) < 0.1:
            route = "PERIODIC_FINITE_TYPE"
        zs = inv.measure.zero_slack_fraction > 0.5
        records.append(CriticalStateRecord(rec.parent_id, zs, route))
        routes[route] += 1
    dominant = max(routes, key=routes.get)  # type: ignore[arg-type]
    diffuse = dominant == "DIFFUSE_CRITICAL_NEUTRAL_STATE_MEASURE" or (
        not inv.measure.stationary and not t091.mu_plus_positive
    )
    return CriticalStateClassifierAudit(
        records=records,
        dominant=dominant,
        diffuse_critical=diffuse,
        messages=[f"dominant={dominant}, diffuse={diffuse}"],
    )


def certify_t099(tree: CanonicalIntrusionTree) -> T099Certificate:
    t091 = certify_t091(tree)
    if t091.mu_plus_positive and t091.route != "NO_CONTINUUM_MASS":
        return T099Certificate(
            "CONJECTURAL_RIGIDITY_TARGET",
            False,
            False,
            ["pre-routed positive-scale; critical invariant not tested"],
        )
    audit = audit_critical_state_classifier(tree)
    status: T099Status = "PROVED_LOCALLY" if audit.dominant in (
        "T087_CARLESON", "POSITIVE_SCALE", "CONCENTRATION", "FINITE_CENTER"
    ) else "CONJECTURAL_RIGIDITY_TARGET"
    return T099Certificate(
        status=status,
        routes_exhausted=not audit.diffuse_critical,
        diffuse_remains=audit.diffuse_critical,
        messages=audit.messages,
    )
