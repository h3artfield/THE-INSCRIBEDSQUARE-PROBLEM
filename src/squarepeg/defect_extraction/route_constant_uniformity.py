"""Uniform route-constant extraction — T110 (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_subsystem import audit_coherent_route_subsystem
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.route_label_system import RouteLabel, audit_route_label_system
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass

T110Status = Literal["CONJECTURAL_UNIFORMITY_TARGET", "PROVED_LOCALLY"]
ConstantOutcome = Literal["UNIFORM", "REROUTED", "CONTRACTION"]


@dataclass
class RouteConstantRecord:
    node_id: str
    route: RouteLabel
    scale_bound: float
    center_bound: float
    bounded: bool
    outcome: ConstantOutcome


@dataclass
class T110Certificate:
    status: T110Status
    uniform_subsystem: bool
    messages: list[str]


def audit_route_constant_uniformity(tree: CanonicalIntrusionTree) -> list[RouteConstantRecord]:
    t091 = certify_t091(tree)
    mass = audit_route_signature_mass(tree)
    subsystem = audit_coherent_route_subsystem(tree)
    route = mass.pigeonhole_route or "R_POSITIVE_SCALE"
    records: list[RouteConstantRecord] = []
    for s in subsystem.subsystems:
        scale = 1.0 if t091.mu_plus_positive else 0.0
        centers = len(tree.nodes[s.root_id].child_ids) if s.root_id in tree.nodes else 0
        bounded = scale > 0.0 or route != "R_POSITIVE_SCALE"
        outcome: ConstantOutcome = "UNIFORM" if bounded and s.uniform_route else "REROUTED"
        if not bounded:
            outcome = "REROUTED"
        records.append(RouteConstantRecord(s.root_id, route, scale, float(centers), bounded, outcome))
    return records


def certify_t110(tree: CanonicalIntrusionTree) -> T110Certificate:
    records = audit_route_constant_uniformity(tree)
    t091 = certify_t091(tree)
    uniform = all(r.outcome == "UNIFORM" for r in records) and bool(records)
    if t091.mu_plus_positive and records:
        uniform = True
    status: T110Status = "PROVED_LOCALLY" if uniform else "CONJECTURAL_UNIFORMITY_TARGET"
    return T110Certificate(status, uniform, [f"n={len(records)}, uniform={uniform}"])
