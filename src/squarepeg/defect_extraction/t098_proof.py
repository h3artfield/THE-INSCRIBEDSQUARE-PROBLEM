"""T097/T098 proof chain and outcome diagnosis (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.bellman_exact_certificate import audit_bellman_exact_certificate
from squarepeg.defect_extraction.bellman_potential import audit_bellman_potential
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.critical_state_classifier import certify_t099
from squarepeg.defect_extraction.neutral_state_cone import audit_neutral_state_cone
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator
from squarepeg.defect_extraction.transition_family import audit_transition_family

T097Status = Literal["CONJECTURAL_STATE_TARGET", "PROVED_LOCALLY"]
T098Status = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]
T089RStatus = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T097Certificate:
    status: T097Status
    recursion_exact: bool
    retained_as_state: bool
    sign_as_state: bool
    messages: list[str]


@dataclass
class T098Certificate:
    status: T098Status
    eta: float
    comparable: bool
    contraction_holds: bool
    messages: list[str]


@dataclass
class T089RBellmanCertificate:
    status: T089RStatus
    via_contraction: bool
    via_critical_rigidity: bool
    messages: list[str]


def certify_t097(tree: CanonicalIntrusionTree) -> T097Certificate:
    cone = audit_neutral_state_cone(tree)
    transfer = audit_neutral_transfer_operator(tree)
    family = audit_transition_family(tree)
    status: T097Status = "PROVED_LOCALLY" if (
        cone.cone_closed and transfer.transfers and family.core_family_size > 0
    ) else "CONJECTURAL_STATE_TARGET"
    return T097Certificate(
        status=status,
        recursion_exact=transfer.recursion_holds,
        retained_as_state=True,
        sign_as_state=True,
        messages=[f"status={status}, transfers={len(transfer.transfers)}"],
    )


def certify_t098(tree: CanonicalIntrusionTree) -> T098Certificate:
    t091 = certify_t091(tree)
    if t091.mu_plus_positive and t091.route != "NO_CONTINUUM_MASS":
        return T098Certificate(
            "CONJECTURAL_CORE_TARGET",
            0.0,
            False,
            False,
            ["positive-scale routed; neutral Bellman not tested"],
        )
    bellman = audit_bellman_potential(tree)
    cert = audit_bellman_exact_certificate(tree, bellman=bellman)
    best = bellman.best
    eta = best.eta if best else 0.0
    holds = bellman.linear_exists and (best.contraction_holds if best else False)
    comparable = best is not None and best.comparable_lower > 0 and best.comparable_upper < 50
    status: T098Status = "PROVED_LOCALLY" if holds and cert.any_verified else "CONJECTURAL_CORE_TARGET"
    return T098Certificate(status, eta, comparable, holds, [f"eta={eta:.3f}, holds={holds}"])


def certify_t089r_bellman(tree: CanonicalIntrusionTree) -> T089RBellmanCertificate:
    t098 = certify_t098(tree)
    t099 = certify_t099(tree)
    via_c = t098.status == "PROVED_LOCALLY" and t098.contraction_holds
    via_r = t099.status == "PROVED_LOCALLY" and t099.routes_exhausted
    status: T089RStatus = "PROVED_LOCALLY" if via_c or via_r else "CONJECTURAL_CORE_TARGET"
    return T089RBellmanCertificate(status, via_c, via_r, [f"contraction={via_c}, rigidity={via_r}"])


def diagnose_d051_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t097 = certify_t097(tree)
    t098 = certify_t098(tree)
    t099 = certify_t099(tree)
    family = audit_transition_family(tree)

    if t097.status != "PROVED_LOCALLY":
        return "E"
    if t098.status == "PROVED_LOCALLY" and t098.contraction_holds:
        return "A"
    if t098.status != "PROVED_LOCALLY" or not t098.contraction_holds:
        return "E"
    if t099.status == "PROVED_LOCALLY" and t099.routes_exhausted:
        return "B"
    if family.core_family_size > 0 and t099.diffuse_remains:
        return "C"
    if t099.diffuse_remains:
        return "D"
    return "E"
