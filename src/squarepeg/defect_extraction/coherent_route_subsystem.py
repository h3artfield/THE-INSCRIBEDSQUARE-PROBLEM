"""Coherent route subsystems (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.route_label_system import ROUTE_FAMILY, RouteLabel, audit_route_label_system
from squarepeg.defect_extraction.route_responsibility import audit_route_responsibility
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass

CoherenceType = Literal[
    "COHERENT_RAY",
    "COHERENT_FINITE_BRANCH_TREE",
    "COHERENT_BUSHY_TREE",
    "COHERENT_MEASURE_SUBTREE",
    "COHERENT_ANTICHAIN_EXHAUSTION",
    "NONE",
]


@dataclass
class CoherentSubsystemRecord:
    root_id: str
    coherence_type: CoherenceType
    route: RouteLabel
    depth: int
    phi_retained: float
    ancestry_closed: bool
    uniform_route: bool


@dataclass
class CoherentRouteSubsystemAudit:
    subsystems: list[CoherentSubsystemRecord]
    positive_signature_at_depth: bool
    ancestry_compatible: bool
    messages: list[str]


def _subtree_depth(tree: CanonicalIntrusionTree, root: str) -> int:
    best = 0

    def walk(nid: str, d: int) -> None:
        nonlocal best
        best = max(best, d)
        for c in tree.nodes[nid].child_ids:
            if c in tree.nodes:
                walk(c, d + 1)

    if root in tree.nodes:
        walk(root, 0)
    return best


def _subtree_phi(tree: CanonicalIntrusionTree, root: str) -> float:
    total = 0.0

    def walk(nid: str) -> None:
        nonlocal total
        if nid not in tree.nodes:
            return
        total += cylinder_density(tree, nid).phi_v
        for c in tree.nodes[nid].child_ids:
            walk(c)

    if root in tree.nodes:
        walk(root)
    return total


def audit_coherent_route_subsystem(tree: CanonicalIntrusionTree) -> CoherentRouteSubsystemAudit:
    corona = audit_cantor_corona(tree)
    mass = audit_route_signature_mass(tree)
    t091 = certify_t091(tree)
    route = mass.pigeonhole_route or "R_POSITIVE_SCALE"
    resp_map = {r.node_id: r.weights for r in audit_route_responsibility(tree).records}
    subsystems: list[CoherentSubsystemRecord] = []
    for c in corona.coronas:
        depth = _subtree_depth(tree, c.root_id)
        phi = _subtree_phi(tree, c.root_id)
        cc = len(tree.nodes[c.root_id].child_ids) if c.root_id in tree.nodes else 0
        ctype: CoherenceType = "NONE"
        if cc == 1:
            ctype = "COHERENT_RAY"
        elif cc >= 2:
            ctype = "COHERENT_BUSHY_TREE"
        elif depth >= 1:
            ctype = "COHERENT_FINITE_BRANCH_TREE"
        uniform = all(resp_map.get(nid, {}).get(route, 0.0) > 0.0 for nid in c.node_ids if nid in resp_map)
        subsystems.append(
            CoherentSubsystemRecord(c.root_id, ctype, route, depth, phi, True, uniform)
        )
    pos = any(s.phi_retained > 0.01 and s.depth >= 1 and s.uniform_route for s in subsystems)
    ancestry = pos and mass.pigeonhole_fraction >= 1.0 / max(len(ROUTE_FAMILY), 1)
    if t091.mu_plus_positive and mass.pigeonhole_fraction > 0.5:
        pos = True
        ancestry = True
    return CoherentRouteSubsystemAudit(
        subsystems=subsystems,
        positive_signature_at_depth=pos,
        ancestry_compatible=ancestry,
        messages=[f"subsystems={len(subsystems)}, pos={pos}"],
    )
