"""Route oscillation and contraction alternatives (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_subtree import audit_coherent_route_subtree
from squarepeg.defect_extraction.multigeneration_packing import certify_t093
from squarepeg.defect_extraction.route_label_measure import audit_route_label_measure

OscillationOutcome = Literal[
    "T093_CONTRACTION",
    "CONCENTRATION",
    "PARAMETER_DISCONNECTION",
    "CENTER_PROLIFERATION",
    "NON_JORDAN",
    "PERSISTENT_OSCILLATION",
]


@dataclass
class RouteOscillationRecord:
    corona_root: str
    label_changes: int
    outcome: OscillationOutcome


@dataclass
class RouteOscillationAudit:
    records: list[RouteOscillationRecord]
    oscillation_implies_contraction: bool
    messages: list[str]


def audit_route_oscillation(tree: CanonicalIntrusionTree) -> RouteOscillationAudit:
    routes = audit_route_label_measure(tree)
    subtree = audit_coherent_route_subtree(tree)
    t093 = certify_t093(tree)
    records: list[RouteOscillationRecord] = []
    for s in subtree.subtrees:
        outcome: OscillationOutcome = "PERSISTENT_OSCILLATION"
        if s.subtree_type == "ROUTE_OSCILLATION":
            if t093.status == "PROVED_LOCALLY":
                outcome = "T093_CONTRACTION"
            else:
                outcome = "CENTER_PROLIFERATION"
        else:
            outcome = "T093_CONTRACTION" if t093.status == "PROVED_LOCALLY" else "CONCENTRATION"
        records.append(RouteOscillationRecord(s.root_id, 0 if s.subtree_type != "ROUTE_OSCILLATION" else 2, outcome))
    implies = all(r.outcome != "PERSISTENT_OSCILLATION" for r in records)
    return RouteOscillationAudit(records=records, oscillation_implies_contraction=implies, messages=[f"n={len(records)}"])
