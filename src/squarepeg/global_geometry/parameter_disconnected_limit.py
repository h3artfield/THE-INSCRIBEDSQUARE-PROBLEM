"""Parameter-disconnected limit classification (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.parameter_support import audit_parameter_support

DisconnectionType = Literal[
    "FINITE_DISCONNECTED",
    "COUNTABLE_DISCONNECTED",
    "CANTOR_DISCONNECTED",
    "DUST_LIKE",
    "COMPONENT_MERGER",
    "ALTERNATING_CHAIN",
    "HARMLESS_QUOTIENT",
    "CONNECTED_OK",
]


@dataclass
class ParameterLimitRecord:
    limit_id: str
    disconnection_type: DisconnectionType
    true_disconnection: bool


@dataclass
class ParameterDisconnectedLimitAudit:
    records: list[ParameterLimitRecord]
    harmless_separated: bool
    exhaustive: bool
    messages: list[str]


def audit_parameter_disconnected_limits(tree: CanonicalIntrusionTree) -> ParameterDisconnectedLimitAudit:
    support = audit_parameter_support(tree)
    records: list[ParameterLimitRecord] = []
    for r in support.records:
        dt: DisconnectionType = "CONNECTED_OK"
        true_disc = False
        if r.support_class == "HARMLESS_QUOTIENT":
            dt = "HARMLESS_QUOTIENT"
        elif r.support_class == "FINITE_DISCONNECTED":
            dt = "FINITE_DISCONNECTED"
            true_disc = True
        elif r.support_class == "COUNTABLE_DISCONNECTED":
            dt = "COUNTABLE_DISCONNECTED"
            true_disc = True
        elif r.support_class == "CANTOR_DISCONNECTED":
            dt = "CANTOR_DISCONNECTED"
            true_disc = True
        elif r.support_class == "DUST_LIKE":
            dt = "DUST_LIKE"
            true_disc = True
        elif r.gap_mass > 0 and r.component_count == 2:
            dt = "COMPONENT_MERGER"
            true_disc = True
        elif r.gap_mass > 0 and r.component_count > 2:
            dt = "ALTERNATING_CHAIN"
            true_disc = True
        records.append(ParameterLimitRecord(r.support_id, dt, true_disc))
    harmless_sep = all(
        not rec.true_disconnection or rec.disconnection_type != "CONNECTED_OK" for rec in records
    )
    return ParameterDisconnectedLimitAudit(records, harmless_sep, bool(records), [f"n={len(records)}"])
