"""T101 — Universal neutral transition exhaustion (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.infinite_dimensional_transition_routes import audit_infinite_dimensional_transition_routes
from squarepeg.defect_extraction.neutral_routing_predicates import audit_neutral_routing_predicates
from squarepeg.defect_extraction.routing_destination_audit import audit_routing_destination
from squarepeg.defect_extraction.transition_interval_certificate import build_interval_certificate

T101Status = Literal["CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "PROVED_FINITE_DOMAIN"]


@dataclass
class T101Certificate:
    status: T101Status
    fixture_coverage: bool
    finite_domain_complete: bool
    infinite_analytic: bool
    messages: list[str]


def certify_t101(tree: CanonicalIntrusionTree) -> T101Certificate:
    pred = audit_neutral_routing_predicates(tree)
    dest = audit_routing_destination(tree)
    cert = build_interval_certificate()
    inf = audit_infinite_dimensional_transition_routes(tree)
    fixture_ok = pred.universal_coverage and dest.all_verified
    finite_ok = cert.complete and cert.unresolved_cells == 0
    if fixture_ok and finite_ok and inf.all_routed_analytically and not inf.infinite_branch_remains:
        status: T101Status = "PROVED_LOCALLY"
    elif fixture_ok and finite_ok:
        status = "PROVED_FINITE_DOMAIN"
    else:
        status = "CONJECTURAL_EXHAUSTION_TARGET"
    return T101Certificate(
        status=status,
        fixture_coverage=fixture_ok,
        finite_domain_complete=finite_ok,
        infinite_analytic=inf.all_routed_analytically,
        messages=[f"fixture={fixture_ok}, finite={finite_ok}, inf={inf.infinite_branch_remains}"],
    )
