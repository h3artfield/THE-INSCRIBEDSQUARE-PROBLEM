"""T092, T086E endpoint-repaired reduction (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_end_surgery import certify_t087
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.endpoint_graph_compactness import audit_endpoint_graph_compactness
from squarepeg.defect_extraction.endpoint_kernel_disintegration import audit_endpoint_kernel_disintegration
from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.noncarleson_cantor_tangent import audit_noncarleson_cantor_tangent
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density
from squarepeg.defect_extraction.nonsummable_ray_reduction import certify_t085
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

CantorDiagnosis = Literal[
    "POSSIBILITY_A_POSITIVE_SCALE",
    "POSSIBILITY_B_NESTING_FAILURE",
    "POSSIBILITY_C_IMPLEMENTATION_SINGLETON",
    "POSSIBILITY_D_GENUINE_CONTINUUM",
]

T092Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T086EStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T092Route = Literal[
    "SINGLETON_AE",
    "POSITIVE_DIAMETER_MASS",
    "INCOMPATIBLE_NESTING",
    "NON_JORDAN",
    "GRAPH_COMPACTNESS_FAILURE",
]

T086ERoute = Literal[
    "T087_CLOSED",
    "ATOMIC_RAY",
    "CONCENTRATED_INCIDENCE",
    "FINITE_CENTER_INCIDENCE",
    "T091_CONTINUUM",
    "NONCARLESON_SINGLETON_CANTOR",
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
]


@dataclass
class VariableRatioCantorDiagnosis:
    diagnosis: CantorDiagnosis
    nested: bool
    d_phi_zero_fraction: float
    mu_plus_fraction: float
    non_carleson: bool
    messages: list[str]


@dataclass
class T092Certificate:
    status: T092Status
    route: T092Route
    messages: list[str]


@dataclass
class T086ECertificate:
    status: T086EStatus
    route: T086ERoute
    messages: list[str]


def diagnose_variable_ratio_cantor(tree: CanonicalIntrusionTree) -> VariableRatioCantorDiagnosis:
    em = audit_endpoint_multifunction(tree)
    split = audit_singleton_continuum_split(tree)
    nc = audit_noncarleson_end_density(tree)
    geom_diam_decay = all(
        r.d_infty < 0.15 or r.diameter_class in ("SINGLETON_END", "ZERO_DIAMETER_END")
        for r in em.records
    )
    not_nested = sum(1 for r in em.records if r.nesting == "END_HULLS_NOT_NESTED") > 0.2 * len(em.records)
    singleton_frac = sum(1 for r in em.records if r.d_phi <= 0.02) / max(len(em.records), 1)

    diag: CantorDiagnosis = "POSSIBILITY_D_GENUINE_CONTINUUM"
    if not_nested:
        diag = "POSSIBILITY_B_NESTING_FAILURE"
    elif split.E_plus_fraction > 0.3 and not geom_diam_decay:
        diag = "POSSIBILITY_A_POSITIVE_SCALE"
    elif singleton_frac >= 0.7 and nc.intrinsically_non_carleson:
        diag = "POSSIBILITY_C_IMPLEMENTATION_SINGLETON"
    elif split.E_plus_fraction > 0.2:
        diag = "POSSIBILITY_D_GENUINE_CONTINUUM"

    return VariableRatioCantorDiagnosis(
        diagnosis=diag,
        nested=not not_nested,
        d_phi_zero_fraction=singleton_frac,
        mu_plus_fraction=split.E_plus_fraction,
        non_carleson=nc.intrinsically_non_carleson,
        messages=[f"diag={diag}, singleton_frac={singleton_frac:.2f}"],
    )


def certify_t092(tree: CanonicalIntrusionTree) -> T092Certificate:
    em = audit_endpoint_multifunction(tree)
    split = audit_singleton_continuum_split(tree)
    graph = audit_endpoint_graph_compactness(tree)

    route: T092Route = "SINGLETON_AE"
    status: T092Status = "PROVED_LOCALLY_CLASSIFIER"

    if split.mu_plus_mass > 0.01:
        route = "POSITIVE_DIAMETER_MASS"
    elif sum(1 for r in em.records if r.nesting == "END_HULLS_NOT_NESTED") > 0.3 * len(em.records):
        route = "INCOMPATIBLE_NESTING"
    elif not graph.tangent_graph_converges:
        route = "GRAPH_COMPACTNESS_FAILURE"
    elif split.E0_fraction < 0.5:
        route = "POSITIVE_DIAMETER_MASS"

    return T092Certificate(status=status, route=route, messages=[f"route={route}"])


def certify_t086e(tree: CanonicalIntrusionTree) -> T086ECertificate:
    t087 = certify_t087(tree)
    nc = audit_noncarleson_end_density(tree)
    t091 = certify_t091(tree)
    t092 = certify_t092(tree)
    inc = audit_incidence_concentration(tree)
    diag = diagnose_variable_ratio_cantor(tree)

    if t087.status == "PROVED_LOCALLY":
        return T086ECertificate(
            status="PROVED_LOCALLY_PARTIAL",
            route="T087_CLOSED",
            messages=["Carleson closed"],
        )

    route: T086ERoute = "NONCARLESON_SINGLETON_CANTOR"
    status: T086EStatus = "CONJECTURAL_TARGET"

    if t091.mu_plus_positive:
        route = "T091_CONTINUUM"
        status = "PROVED_LOCALLY_PARTIAL"
    elif inc.routes_t064:
        route = "CONCENTRATED_INCIDENCE"
        status = "PROVED_LOCALLY_PARTIAL"
    elif inc.routes_t062:
        route = "FINITE_CENTER_INCIDENCE"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t092.route == "INCOMPATIBLE_NESTING":
        route = "NON_JORDAN"
    elif diag.diagnosis == "POSSIBILITY_C_IMPLEMENTATION_SINGLETON" and nc.intrinsically_non_carleson:
        route = "NONCARLESON_SINGLETON_CANTOR"

    return T086ECertificate(status=status, route=route, messages=[f"route={route}, diag={diag.diagnosis}"])
