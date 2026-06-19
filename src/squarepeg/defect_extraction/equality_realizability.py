"""Jordan realizability for equality templates (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.equality_template_classifier import (
    EqualityTemplate,
    audit_equality_template_classifier,
)
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density

ExclusionRoute = Literal[
    "T087_CARLESON",
    "CONCENTRATION",
    "FINITE_CENTER",
    "ANNULAR",
    "THIN",
    "PARAMETER_DISCONNECTED",
    "POSITIVE_SCALE",
    "NON_JORDAN",
    "REALIZABLE_CRITICAL",
    "NOT_REALIZABLE",
]


@dataclass
class RealizabilityRecord:
    template: EqualityTemplate
    jordan_realizable: bool
    exclusion: ExclusionRoute
    messages: list[str]


@dataclass
class EqualityRealizabilityAudit:
    records: list[RealizabilityRecord]
    any_critical_survives: bool
    messages: list[str]


def audit_equality_realizability(tree: CanonicalIntrusionTree) -> EqualityRealizabilityAudit:
    tmpl = audit_equality_template_classifier(tree)
    carl = audit_end_signature_carleson(tree)
    nc = audit_noncarleson_end_density(tree)
    records: list[RealizabilityRecord] = []
    critical = False

    for t in tmpl.templates_found:
        if t == "NOT_EQUALITY":
            continue
        jordan = all(n.jordan_hull for n in tree.nodes.values())
        route: ExclusionRoute = "NOT_REALIZABLE"
        if carl.satisfies_carleson:
            route = "T087_CARLESON"
        elif t == "DOMINANT_RAY_EQUALITY":
            route = "CONCENTRATION"
        elif t in ("ANNULAR_EQUALITY",):
            route = "ANNULAR"
        elif t in ("THIN_PARALLEL_EQUALITY",):
            route = "THIN"
        elif t == "FINITE_CENTER_SELF_SIMILARITY":
            route = "FINITE_CENTER"
        elif t == "INFINITE_CENTER_EQUALITY":
            route = "POSITIVE_SCALE"
        elif t == "NO_JORDAN_REALIZABLE_EQUALITY":
            route = "NON_JORDAN"
        elif nc.intrinsically_non_carleson and jordan and t == "DISJOINT_SELF_SIMILAR_PACKING":
            route = "REALIZABLE_CRITICAL"
            critical = True
        else:
            route = "FINITE_CENTER" if jordan else "NON_JORDAN"
        records.append(
            RealizabilityRecord(t, jordan, route, [f"template={t}, route={route}"])
        )

    return EqualityRealizabilityAudit(
        records=records,
        any_critical_survives=critical,
        messages=[f"records={len(records)}, critical={critical}"],
    )
