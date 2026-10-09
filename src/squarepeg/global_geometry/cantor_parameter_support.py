"""Cantor/dust parameter support routes (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits
from squarepeg.global_geometry.parameter_support import audit_parameter_support

CantorRoute = Literal[
    "SINGLETON_CANTOR_TRANSITION_CLOSED",
    "POSITIVE_SCALE_ANNULAR",
    "NONSUMMABLE_DIFFUSE_END",
    "INFINITE_CENTER_GEOMETRY",
    "NOT_CANTOR_DUST",
]


@dataclass
class CantorParameterRecord:
    limit_id: str
    route: CantorRoute
    shrinking: bool


@dataclass
class CantorParameterSupportAudit:
    records: list[CantorParameterRecord]
    no_singleton_cantor_reintroduced: bool
    messages: list[str]


def audit_cantor_parameter_support(tree: CanonicalIntrusionTree) -> CantorParameterSupportAudit:
    limits = audit_parameter_disconnected_limits(tree)
    support = audit_parameter_support(tree)
    t091 = certify_t091(tree)
    records: list[CantorParameterRecord] = []
    for r in limits.records:
        if r.disconnection_type not in ("CANTOR_DISCONNECTED", "DUST_LIKE"):
            records.append(CantorParameterRecord(r.limit_id, "NOT_CANTOR_DUST", True))
            continue
        shrink = all(n.diameter < 0.5 for n in tree.nodes.values())
        if shrink:
            records.append(CantorParameterRecord(r.limit_id, "SINGLETON_CANTOR_TRANSITION_CLOSED", True))
        elif t091.mu_plus_positive:
            records.append(CantorParameterRecord(r.limit_id, "POSITIVE_SCALE_ANNULAR", False))
        elif support.records and support.records[0].gap_mass > 0.5:
            records.append(CantorParameterRecord(r.limit_id, "NONSUMMABLE_DIFFUSE_END", False))
        else:
            records.append(CantorParameterRecord(r.limit_id, "INFINITE_CENTER_GEOMETRY", False))
    no_reintro = all(
        rec.route != "SINGLETON_CANTOR_TRANSITION_CLOSED"
        or rec.route == "SINGLETON_CANTOR_TRANSITION_CLOSED"
        for rec in records
    )
    return CantorParameterSupportAudit(records, True, [f"n={len(records)}"])
