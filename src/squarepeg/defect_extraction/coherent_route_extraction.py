"""T103 — Coherent route extraction along neutral coronas (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.neutral_routing_predicates import RoutingPredicate, audit_neutral_routing_predicates

T103Status = Literal["CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY"]
CoherentRoute = Literal[
    "SINGLE_BRANCH_SUBSYSTEM",
    "T093_CONTRACTION",
    "GLOBAL_RESIDUAL",
    "MIXED_UNSTABILIZED",
]


@dataclass
class CoherentRouteRecord:
    corona_root: str
    route: CoherentRoute
    dominant_predicate: RoutingPredicate | None
    signature_fraction: float


@dataclass
class CoherentRouteAudit:
    records: list[CoherentRouteRecord]
    stabilized: bool
    messages: list[str]


@dataclass
class T103Certificate:
    status: T103Status
    coherent_subsystem_exists: bool
    messages: list[str]


def audit_coherent_route_extraction(tree: CanonicalIntrusionTree) -> CoherentRouteAudit:
    corona = audit_cantor_corona(tree)
    pred = audit_neutral_routing_predicates(tree)
    route_map = {r.parent_id: r.primary for r in pred.results}
    records: list[CoherentRouteRecord] = []
    for c in corona.coronas:
        preds = [route_map.get(nid) for nid in c.node_ids if nid in route_map]
        preds = [p for p in preds if p and p != "NONE"]
        if not preds:
            records.append(CoherentRouteRecord(c.root_id, "GLOBAL_RESIDUAL", None, 0.0))
            continue
        dominant = max(set(preds), key=preds.count)
        frac = preds.count(dominant) / len(preds)
        route: CoherentRoute = "SINGLE_BRANCH_SUBSYSTEM" if frac >= 0.75 else "MIXED_UNSTABILIZED"
        records.append(CoherentRouteRecord(c.root_id, route, dominant, frac))
    # Fixture-level homogeneity is not universal stabilization.
    stabilized = False
    return CoherentRouteAudit(records=records, stabilized=stabilized, messages=[f"coronas={len(records)}"])


def certify_t103(tree: CanonicalIntrusionTree) -> T103Certificate:
    audit = audit_coherent_route_extraction(tree)
    status: T103Status = "PROVED_LOCALLY" if audit.stabilized else "CONJECTURAL_SELECTION_TARGET"
    coherent = any(r.route == "SINGLE_BRANCH_SUBSYSTEM" for r in audit.records)
    return T103Certificate(status, coherent or audit.stabilized, audit.messages)
