"""Signature-weighted route label mass (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.countable_child_transition_routes import audit_countable_child_transition_routes
from squarepeg.defect_extraction.neutral_routing_predicates import audit_neutral_routing_predicates
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.unbounded_gate_transition_routes import audit_unbounded_gate_transition_routes


@dataclass
class RouteMassSlice:
    depth: int
    label: str
    phi_mass: float
    fraction: float


@dataclass
class RouteLabelMeasureAudit:
    slices: list[RouteMassSlice]
    dominant_label: str | None
    persistent_fraction: float
    messages: list[str]


def audit_route_label_measure(tree: CanonicalIntrusionTree) -> RouteLabelMeasureAudit:
    pred = audit_neutral_routing_predicates(tree)
    child = audit_countable_child_transition_routes(tree)
    gate = audit_unbounded_gate_transition_routes(tree)
    route_map: dict[str, list[str]] = {}
    for r in pred.results:
        route_map.setdefault(r.parent_id, []).append(r.primary)
    for r in child.records:
        route_map.setdefault(r.parent_id, []).append(r.route)
    slices: list[RouteMassSlice] = []
    depth_mass: dict[tuple[int, str], float] = {}
    total = 0.0
    for nid, labels in route_map.items():
        if nid not in tree.nodes:
            continue
        d = cylinder_density(tree, nid).depth
        phi = cylinder_density(tree, nid).phi_v
        total += phi
        for lab in labels:
            depth_mass[(d, lab)] = depth_mass.get((d, lab), 0.0) + phi / max(len(labels), 1)
    for (d, lab), mass in depth_mass.items():
        slices.append(RouteMassSlice(d, lab, mass, mass / max(total, 1e-12)))
    by_label: dict[str, float] = {}
    for s in slices:
        by_label[s.label] = by_label.get(s.label, 0.0) + s.phi_mass
    dominant = max(by_label, key=by_label.get) if by_label else None  # type: ignore[arg-type]
    frac = by_label.get(dominant, 0.0) / max(total, 1e-12) if dominant else 0.0
    return RouteLabelMeasureAudit(
        slices=slices,
        dominant_label=dominant,
        persistent_fraction=frac,
        messages=[f"slices={len(slices)}, dominant={dominant}"],
    )
