"""T094 proof chain (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.equality_realizability import audit_equality_realizability
from squarepeg.defect_extraction.equality_template_classifier import audit_equality_template_classifier
from squarepeg.defect_extraction.multigeneration_packing import certify_t093
from squarepeg.defect_extraction.neutral_corona_tangent import audit_neutral_corona_tangent
from squarepeg.defect_extraction.t093_coverage_audit import audit_t093_coverage

T094Status = Literal["CONJECTURAL_RIGIDITY_TARGET", "PROVED_LOCALLY"]
T094Route = Literal[
    "T087_CARLESON",
    "CONCENTRATION",
    "FINITE_CENTER",
    "ANNULAR_THIN",
    "PARAMETER_DISCONNECTED",
    "POSITIVE_SCALE",
    "NON_JORDAN",
    "CRITICAL_EQUALITY_REMAINS",
]


@dataclass
class T094Certificate:
    status: T094Status
    route: T094Route
    t094a_holds: bool
    chain_complete: bool
    messages: list[str]


@dataclass
class T089RClosureCertificate:
    status: Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]
    t093_closed: bool
    t094_closed: bool
    neutral_residual_eliminated: bool
    messages: list[str]


def certify_t094(tree: CanonicalIntrusionTree) -> T094Certificate:
    t091 = certify_t091(tree)
    if t091.mu_plus_positive:
        return T094Certificate(
            "PROVED_LOCALLY", "POSITIVE_SCALE", False, True, ["T091 continuum"]
        )
    coverage = audit_t093_coverage(tree)
    tangent = audit_neutral_corona_tangent(tree)
    tmpl = audit_equality_template_classifier(tree)
    real = audit_equality_realizability(tree)

    t094a = tangent.compactness_holds and tangent.all_deficits_vanish
    if real.any_critical_survives:
        return T094Certificate(
            "CONJECTURAL_RIGIDITY_TARGET",
            "CRITICAL_EQUALITY_REMAINS",
            t094a,
            False,
            ["critical template survives realizability audit"],
        )
    if coverage.residual_in_neutral and not tmpl.exhaustive:
        return T094Certificate(
            "CONJECTURAL_RIGIDITY_TARGET",
            "CRITICAL_EQUALITY_REMAINS",
            t094a,
            False,
            ["residual neutral phi; template list not exhaustive"],
        )
    route: T094Route = "FINITE_CENTER"
    status: T094Status = "PROVED_LOCALLY"
    for rec in real.records:
        if rec.exclusion == "T087_CARLESON":
            route = "T087_CARLESON"
        elif rec.exclusion == "CONCENTRATION":
            route = "CONCENTRATION"
        elif rec.exclusion in ("ANNULAR", "THIN"):
            route = "ANNULAR_THIN"
    return T094Certificate(status, route, t094a, True, ["equality routed"])


def certify_t089r_closure(tree: CanonicalIntrusionTree) -> T089RClosureCertificate:
    t093 = certify_t093(tree)
    t094 = certify_t094(tree)
    coverage = audit_t093_coverage(tree)
    from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density

    nc = audit_noncarleson_end_density(tree)
    closed = (
        t093.status == "PROVED_LOCALLY"
        and t094.status == "PROVED_LOCALLY"
        and t094.chain_complete
        and t094.t094a_holds
        and t094.route not in ("CRITICAL_EQUALITY_REMAINS", "POSITIVE_SCALE")
        and not coverage.residual_in_neutral
        and not nc.intrinsically_non_carleson
    )
    return T089RClosureCertificate(
        status="PROVED_LOCALLY" if closed else "CONJECTURAL_CORE_TARGET",
        t093_closed=t093.status == "PROVED_LOCALLY",
        t094_closed=t094.status == "PROVED_LOCALLY" and t094.chain_complete,
        neutral_residual_eliminated=not coverage.residual_in_neutral,
        messages=[
            f"t093={t093.status}, t094={t094.status}, neutral_residual={coverage.residual_in_neutral}",
        ],
    )


def diagnose_d049_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t094 = certify_t094(tree)
    t089 = certify_t089r_closure(tree)
    from squarepeg.defect_extraction.critical_equality_models import audit_critical_equality_models
    from squarepeg.defect_extraction.equality_compatibility import audit_equality_compatibility
    from squarepeg.defect_extraction.neutral_corona_tangent import audit_neutral_corona_tangent
    from squarepeg.defect_extraction.t094_clean_room import audit_t094_clean_room

    crit = audit_critical_equality_models()
    tangent = audit_neutral_corona_tangent(tree)
    tmpl = audit_equality_template_classifier(tree)
    clean = audit_t094_clean_room(tree)

    if t089.status == "PROVED_LOCALLY" and clean.verdict == "T094_CLEAN_ROOM_VERIFIED":
        return "A"
    if t094.status == "PROVED_LOCALLY" and tmpl.exhaustive and t094.t094a_holds and t094.route not in (
        "CRITICAL_EQUALITY_REMAINS",
        "POSITIVE_SCALE",
    ):
        return "B"
    if tmpl.templates_found and t094.route == "CRITICAL_EQUALITY_REMAINS":
        return "C"
    if crit.countermodel_found:
        return "D"
    if not t094.t094a_holds or not tangent.all_deficits_vanish or clean.verdict != "T094_CLEAN_ROOM_VERIFIED":
        return "E"
    return "E"
