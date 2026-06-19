"""Multigeneration singleton rigidity — T089R via T093/T094, T086M (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.critical_equality_rigidity import certify_t094
from squarepeg.defect_extraction.multigeneration_packing import certify_t093
from squarepeg.defect_extraction.neutral_corona_compactness import audit_neutral_corona_compactness
from squarepeg.defect_extraction.singleton_end_rigidity import certify_t089r_singleton
from squarepeg.defect_extraction.singleton_frostman_criterion import certify_t090r_singleton

T089RStatus = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]
T086MStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T086MRoute = Literal[
    "T093_MULTIGEN",
    "T087_CARLESON",
    "CONCENTRATION",
    "FINITE_CENTER",
    "ANNULAR_THIN",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "INFINITE_CENTER",
    "CRITICAL_EQUALITY",
    "T091_CONTINUUM",
]


@dataclass
class T089RMultigenCertificate:
    status: T089RStatus
    via_t093: bool
    via_t094: bool
    messages: list[str]


@dataclass
class T086MCertificate:
    status: T086MStatus
    route: T086MRoute
    messages: list[str]


def certify_t089r_multigen(tree: CanonicalIntrusionTree) -> T089RMultigenCertificate:
    t091 = certify_t091(tree)
    if t091.mu_plus_positive:
        return T089RMultigenCertificate(
            "CONJECTURAL_CORE_TARGET", False, False, ["continuum via T091"]
        )
    t093 = certify_t093(tree)
    t094 = certify_t094(tree)
    base = certify_t089r_singleton(tree)
    if t093.status == "PROVED_LOCALLY" and t093.multigen_holds:
        return T089RMultigenCertificate("PROVED_LOCALLY", True, False, t093.messages)
    if t094.status == "PROVED_LOCALLY_CLASSIFIER" and t094.route != "CRITICAL_MODEL_REMAINS":
        return T089RMultigenCertificate("PROVED_LOCALLY", False, True, t094.messages)
    if base.status == "PROVED_LOCALLY":
        return T089RMultigenCertificate("PROVED_LOCALLY", False, False, base.messages)
    return T089RMultigenCertificate(
        "CONJECTURAL_CORE_TARGET",
        t093.multigen_holds,
        t094.critical_model_found,
        ["T089R open; neutral corona or equality model"],
    )


def certify_t086m(tree: CanonicalIntrusionTree) -> T086MCertificate:
    t091 = certify_t091(tree)
    if t091.mu_plus_positive:
        return T086MCertificate("PROVED_LOCALLY_PARTIAL", "T091_CONTINUUM", ["T091"])
    t093 = certify_t093(tree)
    t094 = certify_t094(tree)
    t089 = certify_t089r_multigen(tree)
    t090 = certify_t090r_singleton(tree)
    neutral = audit_neutral_corona_compactness(tree)

    if t093.status == "PROVED_LOCALLY":
        return T086MCertificate("PROVED_LOCALLY_PARTIAL", "T093_MULTIGEN", t093.messages)
    if t090.implies_carleson:
        return T086MCertificate("PROVED_LOCALLY_PARTIAL", "T087_CARLESON", t090.messages)
    if t094.route == "CONCENTRATION":
        return T086MCertificate("PROVED_LOCALLY_PARTIAL", "CONCENTRATION", t094.messages)
    if t094.route == "FINITE_CENTER":
        return T086MCertificate("PROVED_LOCALLY_PARTIAL", "FINITE_CENTER", t094.messages)
    if t094.route == "ANNULAR_THIN":
        return T086MCertificate("PROVED_LOCALLY_PARTIAL", "ANNULAR_THIN", t094.messages)
    if not neutral.compactness_holds and neutral.long_corona_exists:
        return T086MCertificate(
            "CONJECTURAL_STRUCTURAL_TARGET", "INFINITE_CENTER", neutral.messages
        )
    if t094.critical_model_found or t094.route == "CRITICAL_MODEL_REMAINS":
        return T086MCertificate(
            "CONJECTURAL_STRUCTURAL_TARGET", "CRITICAL_EQUALITY", t094.messages
        )
    return T086MCertificate(
        "CONJECTURAL_STRUCTURAL_TARGET",
        "CRITICAL_EQUALITY",
        ["multigeneration packing not closed"],
    )


def diagnose_d048_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t093 = certify_t093(tree)
    t094 = certify_t094(tree)
    t089 = certify_t089r_multigen(tree)
    from squarepeg.defect_extraction.signature_budget import audit_signature_budget
    from squarepeg.defect_extraction.neutral_corona_compactness import audit_neutral_corona_compactness

    budget = audit_signature_budget(tree)
    neutral = audit_neutral_corona_compactness(tree)

    if t089.status == "PROVED_LOCALLY" and t093.status == "PROVED_LOCALLY" and t094.status == "PROVED_LOCALLY_CLASSIFIER":
        return "A"
    if t093.status == "PROVED_LOCALLY":
        return "B"
    if t094.status == "PROVED_LOCALLY_CLASSIFIER" and t094.route != "CRITICAL_MODEL_REMAINS":
        return "C"
    if t094.critical_model_found:
        return "D"
    if not budget.all_balanced or not t093.multigen_holds or not neutral.compactness_holds:
        return "E"
    return "E"
