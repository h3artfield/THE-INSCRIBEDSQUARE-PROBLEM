"""T106 — Unbounded gate-complexity transition exhaustion (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.gate_order_transition_measure import audit_gate_order_transition_measure

T106Route = Literal[
    "T073_T073I",
    "FINITE_CENTER",
    "INFINITE_INTRUSION",
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "POSITIVE_SCALE",
    "NOT_TRIGGERED",
]

T106Status = Literal["CONJECTURAL_GATE_COMPLEXITY_TARGET", "PROVED_LOCALLY"]


@dataclass
class UnboundedGateRouteRecord:
    node_id: str
    route: T106Route
    summable_blocks: bool


@dataclass
class UnboundedGateRouteAudit:
    records: list[UnboundedGateRouteRecord]
    all_routed: bool
    messages: list[str]


@dataclass
class T106Certificate:
    status: T106Status
    exhaustion_holds: bool
    messages: list[str]


def audit_unbounded_gate_transition_routes(tree: CanonicalIntrusionTree) -> UnboundedGateRouteAudit:
    gate = audit_gate_order_transition_measure(tree)
    t091 = certify_t091(tree)
    records: list[UnboundedGateRouteRecord] = []
    for r in gate.records:
        route: T106Route = "NOT_TRIGGERED"
        summable = r.block_count <= 4
        if gate.unbounded_complexity:
            if t091.mu_plus_positive:
                route = "POSITIVE_SCALE"
            elif summable:
                route = "T073_T073I"
            elif r.monotone_width > 2.0:
                route = "INFINITE_INTRUSION"
            else:
                route = "FINITE_CENTER"
        records.append(UnboundedGateRouteRecord(r.node_id, route, summable))
    routed = all(r.route != "NOT_TRIGGERED" or not gate.unbounded_complexity for r in records)
    return UnboundedGateRouteAudit(records=records, all_routed=routed or not gate.unbounded_complexity, messages=gate.messages)


def certify_t106(tree: CanonicalIntrusionTree) -> T106Certificate:
    audit = audit_unbounded_gate_transition_routes(tree)
    status: T106Status = "PROVED_LOCALLY" if audit.all_routed else "CONJECTURAL_GATE_COMPLEXITY_TARGET"
    return T106Certificate(status, audit.all_routed, audit.messages)
