"""T086S / T084S singleton Cantor reduction (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.critical_singleton_tangent import audit_critical_singleton_tangent
from squarepeg.defect_extraction.finite_center_density_improvement import audit_finite_center_density_improvement
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.self_similar_end_models import audit_self_similar_end_models
from squarepeg.defect_extraction.singleton_end_rigidity import certify_t089r_singleton
from squarepeg.defect_extraction.singleton_frostman_criterion import certify_t090r_singleton
from squarepeg.defect_extraction.tangent_of_tangent import audit_tangent_of_tangent

T086SStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T084SStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T086SRoute = Literal[
    "CONCENTRATION",
    "FINITE_CENTER",
    "T089R_DENSITY",
    "T090R_FROSTMAN",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "INFINITE_CENTER",
    "CRITICAL_SINGLETON_CANTOR",
    "T091_CONTINUUM",
]

T084SRoute = Literal[
    "T086S",
    "T091_CONTINUUM",
    "GLOBAL_RESIDUAL",
]


@dataclass
class T086SCertificate:
    status: T086SStatus
    route: T086SRoute
    messages: list[str]


@dataclass
class T084SCertificate:
    status: T084SStatus
    route: T084SRoute
    messages: list[str]


def certify_t086s(tree: CanonicalIntrusionTree) -> T086SCertificate:
    t089 = certify_t089r_singleton(tree)
    t090 = certify_t090r_singleton(tree)
    t091 = certify_t091(tree)
    inc = audit_incidence_concentration(tree)
    imp = audit_finite_center_density_improvement(tree)
    crit = audit_critical_singleton_tangent(tree)
    tot = audit_tangent_of_tangent(tree)

    if t091.mu_plus_positive:
        return T086SCertificate(
            status="PROVED_LOCALLY_PARTIAL",
            route="T091_CONTINUUM",
            messages=["continuum via T091"],
        )
    if t089.route == "CONCENTRATION":
        return T086SCertificate(status="PROVED_LOCALLY_PARTIAL", route="CONCENTRATION", messages=["concentrated"])
    if t089.route == "FINITE_CENTER":
        return T086SCertificate(status="PROVED_LOCALLY_PARTIAL", route="FINITE_CENTER", messages=["finite-center"])
    if t089.route == "DENSITY_IMPROVEMENT" or imp.any_improvement:
        return T086SCertificate(status="PROVED_LOCALLY_PARTIAL", route="T089R_DENSITY", messages=["density gain"])
    if t090.implies_carleson:
        return T086SCertificate(status="PROVED_LOCALLY_PARTIAL", route="T090R_FROSTMAN", messages=["Frostman closed"])
    if tot.records and not tot.compactness_holds:
        return T086SCertificate(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            route="INFINITE_CENTER",
            messages=["tangent-of-tangent compactness failure"],
        )
    if crit.is_critical_residual:
        return T086SCertificate(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            route="CRITICAL_SINGLETON_CANTOR",
            messages=["exact critical singleton residual"],
        )
    if t089.route == "PERSISTENT_NONCARLESON":
        return T086SCertificate(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            route="CRITICAL_SINGLETON_CANTOR",
            messages=["persistent non-Carleson singleton"],
        )
    return T086SCertificate(
        status="CONJECTURAL_STRUCTURAL_TARGET",
        route="CRITICAL_SINGLETON_CANTOR",
        messages=["unresolved singleton Cantor"],
    )


def certify_t084s(tree: CanonicalIntrusionTree) -> T084SCertificate:
    t086 = certify_t086s(tree)
    t091 = certify_t091(tree)
    if t091.mu_plus_positive:
        return T084SCertificate(
            status="PROVED_LOCALLY_PARTIAL",
            route="T091_CONTINUUM",
            messages=["continuum positive-scale"],
        )
    if t086.status == "PROVED_LOCALLY_PARTIAL":
        return T084SCertificate(status="PROVED_LOCALLY_PARTIAL", route="T086S", messages=[f"via {t086.route}"])
    return T084SCertificate(
        status="CONJECTURAL_TARGET",
        route="GLOBAL_RESIDUAL",
        messages=[f"residual {t086.route}"],
    )


def diagnose_d047_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    """Select Directive 047 outcome from audits."""
    from squarepeg.defect_extraction.child_signature_packing import audit_child_signature_packing
    from squarepeg.defect_extraction.end_density_martingale import audit_end_density_martingale

    t089 = certify_t089r_singleton(tree)
    t090 = certify_t090r_singleton(tree)
    packing = audit_child_signature_packing(tree)
    mart = audit_end_density_martingale(tree)
    tot = audit_tangent_of_tangent(tree)
    models = audit_self_similar_end_models()
    crit = audit_critical_singleton_tangent(tree)

    if t089.status == "PROVED_LOCALLY" and t090.status == "PROVED_LOCALLY":
        return "A"
    if t089.status == "PROVED_LOCALLY":
        return "B"
    if t090.status == "PROVED_LOCALLY" and t090.implies_carleson:
        return "C"
    if models.result == "SELF_SIMILAR_CRITICAL_COUNTERMODEL" and crit.is_critical_residual:
        return "D"
    if packing.status == "NO_CONTRACTION" or mart.classification == "NONE":
        return "E"
    if not tot.compactness_holds:
        return "E"
    return "E"
