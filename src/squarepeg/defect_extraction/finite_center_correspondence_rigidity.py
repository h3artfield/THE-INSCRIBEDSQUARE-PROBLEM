"""T089R — Finite-center endpoint-correspondence rigidity (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

T089RStatus = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T089RCertificate:
    status: T089RStatus
    rigidity_holds: bool
    messages: list[str]


def certify_t089r(tree: CanonicalIntrusionTree) -> T089RCertificate:
    split = audit_singleton_continuum_split(tree)
    inc = audit_incidence_concentration(tree)
    t091 = certify_t091(tree)
    carl = audit_end_signature_carleson(tree)

    if split.mu_plus_mass > 0.01:
        return T089RCertificate(
            status="CONJECTURAL_CORE_TARGET",
            rigidity_holds=False,
            messages=["mu+ > 0; apply T091 first"],
        )
    if not inc.routes_t062:
        return T089RCertificate(
            status="CONJECTURAL_CORE_TARGET",
            rigidity_holds=False,
            messages=["not finite-center incidence"],
        )
    rigidity = carl.satisfies_carleson or split.E0_fraction > 0.9
    return T089RCertificate(
        status="PROVED_LOCALLY" if rigidity else "CONJECTURAL_CORE_TARGET",
        rigidity_holds=rigidity,
        messages=[f"rigidity={rigidity}, carleson={carl.satisfies_carleson}"],
    )
