"""T102 — Empty neutral-core theorem (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.compact_neutral_core import audit_compact_neutral_core
from squarepeg.defect_extraction.neutral_routing_predicates import audit_neutral_routing_predicates
from squarepeg.defect_extraction.transition_interval_certificate import build_interval_certificate
from squarepeg.defect_extraction.universal_transition_exhaustion import certify_t101

T102Status = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY", "PROVED_FINITE_DOMAIN"]


@dataclass
class EmptyNeutralCoreAudit:
    core_empty_fixture: bool
    core_empty_definition: bool
    intrinsic_definition: bool
    messages: list[str]


@dataclass
class T102Certificate:
    status: T102Status
    core_empty: bool
    retires_t097c: bool
    messages: list[str]


def audit_empty_neutral_core(tree: CanonicalIntrusionTree) -> EmptyNeutralCoreAudit:
    core = audit_compact_neutral_core(tree)
    pred = audit_neutral_routing_predicates(tree)
    cert = build_interval_certificate()
    fixture_empty = core.core_size == 0
    def_empty = pred.universal_coverage and cert.complete
    return EmptyNeutralCoreAudit(
        core_empty_fixture=fixture_empty,
        core_empty_definition=def_empty,
        intrinsic_definition=def_empty,
        messages=[f"fixture_empty={fixture_empty}, def_empty={def_empty}"],
    )


def certify_t102(tree: CanonicalIntrusionTree) -> T102Certificate:
    t101 = certify_t101(tree)
    audit = audit_empty_neutral_core(tree)
    if t101.status == "PROVED_LOCALLY" and audit.intrinsic_definition:
        status: T102Status = "PROVED_LOCALLY"
    elif t101.status == "PROVED_FINITE_DOMAIN" and audit.core_empty_definition:
        status = "PROVED_FINITE_DOMAIN"
    else:
        status = "CONJECTURAL_CORE_TARGET"
    empty = audit.core_empty_fixture and audit.core_empty_definition
    return T102Certificate(
        status=status,
        core_empty=empty,
        retires_t097c=status in ("PROVED_LOCALLY", "PROVED_FINITE_DOMAIN"),
        messages=audit.messages,
    )
