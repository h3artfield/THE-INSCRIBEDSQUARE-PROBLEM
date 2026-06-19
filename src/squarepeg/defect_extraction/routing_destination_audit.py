"""Routing destination theorem verification (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_routing_predicates import RoutingPredicate, audit_neutral_routing_predicates

Destination = Literal[
    "T064_T085",
    "T091",
    "T085_PLATEAU",
    "T081I",
    "T062_T089R",
    "INFINITE_CENTER_RESIDUAL",
    "T068I_T073I",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_RESIDUAL",
    "COBOUNDARY_QUOTIENT",
    "UNRESOLVED",
]

_PRED_DEST: dict[RoutingPredicate, Destination] = {
    "P_concentration": "T064_T085",
    "P_positive_scale": "T091",
    "P_plateau": "T085_PLATEAU",
    "P_summable_children": "T081I",
    "P_finite_center": "T062_T089R",
    "P_infinite_center": "INFINITE_CENTER_RESIDUAL",
    "P_gate_parameter_escape": "T068I_T073I",
    "P_parameter_disconnected": "PARAMETER_DISCONNECTED",
    "P_non_jordan": "NON_JORDAN_RESIDUAL",
    "P_bookkeeping_coboundary": "COBOUNDARY_QUOTIENT",
    "NONE": "UNRESOLVED",
}


@dataclass
class RoutingDestinationRecord:
    parent_id: str
    predicate: RoutingPredicate
    destination: Destination
    hypotheses_satisfied: bool
    local_routing: bool
    signature_preserved: bool


@dataclass
class RoutingDestinationAudit:
    records: list[RoutingDestinationRecord]
    all_verified: bool
    unresolved_count: int
    messages: list[str]


def audit_routing_destination(tree: CanonicalIntrusionTree) -> RoutingDestinationAudit:
    pred = audit_neutral_routing_predicates(tree)
    records: list[RoutingDestinationRecord] = []
    unresolved = 0
    for res in pred.results:
        for pe in res.predicates:
            dest = _PRED_DEST.get(pe.predicate, "UNRESOLVED")
            ok = dest != "UNRESOLVED" and pe.satisfied
            if not ok:
                unresolved += 1
            records.append(
                RoutingDestinationRecord(
                    res.parent_id,
                    pe.predicate,
                    dest,
                    ok,
                    not pe.requires_subsequence,
                    pe.preserves_signature,
                )
            )
    return RoutingDestinationAudit(
        records=records,
        all_verified=unresolved == 0 and bool(records),
        unresolved_count=unresolved,
        messages=[f"records={len(records)}, unresolved={unresolved}"],
    )
