"""Geometric route-change cost Osc(v,w) (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.route_label_system import RouteLabel, audit_route_label_system
from squarepeg.defect_extraction.route_responsibility import audit_route_responsibility
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass

OscillationClass = Literal[
    "FINITE_ROUTE_OSCILLATION",
    "DIVERGENT_ROUTE_OSCILLATION",
    "DIFFUSE_ROUTE_OSCILLATION",
    "BOUNDARY_ROUTE_OSCILLATION",
]


@dataclass
class RouteOscCostRecord:
    parent_id: str
    child_id: str
    cost: float
    scale_change: float
    route_change: float


@dataclass
class RouteOscillationCostAudit:
    records: list[RouteOscCostRecord]
    total_cost: float
    oscillation_class: OscillationClass
    geometric: bool
    messages: list[str]


def _dominant_route(weights: dict[RouteLabel, float]) -> RouteLabel | None:
    if not weights:
        return None
    return max(weights, key=weights.get)  # type: ignore[arg-type]


def audit_route_oscillation_cost(tree: CanonicalIntrusionTree) -> RouteOscillationCostAudit:
    resp = {r.node_id: r.weights for r in audit_route_responsibility(tree).records}
    states = {s.node_id: s for s in audit_augmented_neutral_state(tree).states}
    records: list[RouteOscCostRecord] = []
    total = 0.0
    changes = 0
    for nid, node in tree.nodes.items():
        pr = _dominant_route(resp.get(nid, {}))
        for cid in node.child_ids:
            if cid not in tree.nodes:
                continue
            cr = _dominant_route(resp.get(cid, {}))
            ps = states[nid].Phi if nid in states else 0.0
            cs = states[cid].Phi if cid in states else 0.0
            scale_chg = abs(ps - cs) / max(ps, cs, 1e-12)
            route_chg = 0.0 if pr == cr else 1.0
            cost = scale_chg + route_chg
            if route_chg > 0:
                changes += 1
            total += cost
            records.append(RouteOscCostRecord(nid, cid, cost, scale_chg, route_chg))
    oclass: OscillationClass = "FINITE_ROUTE_OSCILLATION"
    if changes > len(tree.nodes):
        oclass = "DIVERGENT_ROUTE_OSCILLATION"
    elif changes == 0:
        oclass = "FINITE_ROUTE_OSCILLATION"
    mass = audit_route_signature_mass(tree)
    if mass.pigeonhole_fraction > 0.9 and changes == 0:
        oclass = "FINITE_ROUTE_OSCILLATION"
    return RouteOscillationCostAudit(
        records=records,
        total_cost=total,
        oscillation_class=oclass,
        geometric=True,
        messages=[f"edges={len(records)}, changes={changes}"],
    )
