"""Signature-weighted route mass M_r(n) (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.route_label_system import ROUTE_FAMILY, RouteLabel
from squarepeg.defect_extraction.route_responsibility import audit_route_responsibility


@dataclass
class RouteMassSlice:
    depth: int
    route: RouteLabel
    phi_mass: float
    fraction: float


@dataclass
class RouteSignatureMassAudit:
    slices: list[RouteMassSlice]
    total_phi: float
    mass_conserved: bool
    pigeonhole_route: RouteLabel | None
    pigeonhole_fraction: float
    messages: list[str]


def audit_route_signature_mass(tree: CanonicalIntrusionTree) -> RouteSignatureMassAudit:
    resp = audit_route_responsibility(tree)
    by_depth_route: dict[tuple[int, RouteLabel], float] = {}
    total = 0.0
    for rec in resp.records:
        if rec.node_id not in tree.nodes:
            continue
        phi = cylinder_density(tree, rec.node_id).phi_v
        depth = cylinder_density(tree, rec.node_id).depth
        total += phi
        for lab, w in rec.weights.items():
            key = (depth, lab)
            by_depth_route[key] = by_depth_route.get(key, 0.0) + w * phi
    slices: list[RouteMassSlice] = []
    for (d, lab), mass in by_depth_route.items():
        slices.append(RouteMassSlice(d, lab, mass, mass / max(total, 1e-12)))
    by_route: dict[RouteLabel, float] = {r: 0.0 for r in ROUTE_FAMILY}
    for s in slices:
        by_route[s.route] = by_route.get(s.route, 0.0) + s.phi_mass
    pigeonhole = max(by_route, key=by_route.get) if by_route else None  # type: ignore[arg-type]
    frac = by_route.get(pigeonhole, 0.0) / max(total, 1e-12) if pigeonhole else 0.0
    conserved = abs(sum(by_route.values()) - total) < 1e-6 or total == 0.0
    return RouteSignatureMassAudit(
        slices=slices,
        total_phi=total,
        mass_conserved=conserved,
        pigeonhole_route=pigeonhole,
        pigeonhole_fraction=frac,
        messages=[f"total={total:.4f}, pigeonhole={pigeonhole}, frac={frac:.4f}"],
    )
