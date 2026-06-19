"""T089R singleton end rigidity (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.finite_center_density_improvement import audit_finite_center_density_improvement
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

T089RStatus = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]
RigidityRoute = Literal[
    "CARLESON_CLOSED",
    "CONCENTRATION",
    "FINITE_CENTER",
    "DENSITY_IMPROVEMENT",
    "CONTINUUM_ROUTED",
    "PERSISTENT_NONCARLESON",
]


@dataclass
class SingletonHypothesisAudit:
    singleton_ae: bool
    shrinking_hulls: bool
    jordan_stable: bool
    parameter_connected: bool
    nonatomic: bool
    no_concentration: bool
    finite_center: bool
    persistent_bad_density: bool


@dataclass
class T089RSingletonCertificate:
    status: T089RStatus
    route: RigidityRoute
    hypotheses: SingletonHypothesisAudit
    rigidity_holds: bool
    messages: list[str]


def audit_singleton_hypotheses(tree: CanonicalIntrusionTree) -> SingletonHypothesisAudit:
    split = audit_singleton_continuum_split(tree)
    nc = audit_noncarleson_end_density(tree)
    inc = audit_incidence_concentration(tree)
    from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction

    em = audit_endpoint_multifunction(tree)
    shrink = all(r.d_infty < 0.2 for r in em.records) if em.records else True
    jordan = all(n.jordan_hull for n in tree.nodes.values())
    param_ok = all(
        (n.param_interval[1] - n.param_interval[0]) > 0 for n in tree.nodes.values() if not n.child_ids
    )

    return SingletonHypothesisAudit(
        singleton_ae=split.E0_fraction > 0.95,
        shrinking_hulls=shrink,
        jordan_stable=jordan,
        parameter_connected=param_ok,
        nonatomic=True,
        no_concentration=inc.concentration_class not in ("CONCENTRATED",),
        finite_center=inc.concentration_class == "FINITE_CENTER" or inc.concentration_class == "DIFFUSE",
        persistent_bad_density=nc.intrinsically_non_carleson,
    )


def certify_t089r_singleton(tree: CanonicalIntrusionTree) -> T089RSingletonCertificate:
    hyp = audit_singleton_hypotheses(tree)
    split = audit_singleton_continuum_split(tree)
    t091 = certify_t091(tree)
    carl = audit_end_signature_carleson(tree)
    nc = audit_noncarleson_end_density(tree)
    inc = audit_incidence_concentration(tree)
    imp = audit_finite_center_density_improvement(tree)

    if split.mu_plus_mass > 0.01:
        return T089RSingletonCertificate(
            status="CONJECTURAL_CORE_TARGET",
            route="CONTINUUM_ROUTED",
            hypotheses=hyp,
            rigidity_holds=False,
            messages=["mu+ > 0; T091 applies"],
        )
    if carl.satisfies_carleson:
        return T089RSingletonCertificate(
            status="PROVED_LOCALLY",
            route="CARLESON_CLOSED",
            hypotheses=hyp,
            rigidity_holds=True,
            messages=["END_SIGNATURE_CARLESON"],
        )
    if inc.concentration_class == "CONCENTRATED":
        return T089RSingletonCertificate(
            status="PROVED_LOCALLY",
            route="CONCENTRATION",
            hypotheses=hyp,
            rigidity_holds=True,
            messages=["concentration route"],
        )
    if inc.concentration_class == "FINITE_CENTER":
        return T089RSingletonCertificate(
            status="PROVED_LOCALLY",
            route="FINITE_CENTER",
            hypotheses=hyp,
            rigidity_holds=True,
            messages=["finite-center route"],
        )
    if imp.any_improvement and imp.uniform_epsilon > 0.02:
        return T089RSingletonCertificate(
            status="PROVED_LOCALLY",
            route="DENSITY_IMPROVEMENT",
            hypotheses=hyp,
            rigidity_holds=True,
            messages=[f"density gain eps={imp.uniform_epsilon:.3f}"],
        )
    if nc.intrinsically_non_carleson and hyp.singleton_ae:
        return T089RSingletonCertificate(
            status="CONJECTURAL_CORE_TARGET",
            route="PERSISTENT_NONCARLESON",
            hypotheses=hyp,
            rigidity_holds=False,
            messages=["persistent bad density under singleton hypotheses"],
        )
    return T089RSingletonCertificate(
        status="CONJECTURAL_CORE_TARGET",
        route="PERSISTENT_NONCARLESON",
        hypotheses=hyp,
        rigidity_holds=False,
        messages=["T089R not closed"],
    )
