"""Signature-weighted route density — T109 (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.route_label_system import RouteLabel, audit_route_label_system
from squarepeg.defect_extraction.route_responsibility import audit_route_responsibility
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass

DensityOutcome = Literal[
    "UNIFORM_POSITIVE",
    "BOUNDARY_CONCENTRATED",
    "INCOMPARABLE_DISPERSAL",
    "ZERO_DENSITY",
]

CoherenceExtract = Literal[
    "COHERENT_SUBSYSTEM",
    "CONCENTRATED_DESCENDANT",
    "FINITE_CENTER_SPLIT",
    "BUSHY_MEASURE",
    "ROUTE_OSCILLATION",
    "NONE",
]

T109Status = Literal["CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class RouteDensityRecord:
    node_id: str
    route: RouteLabel
    density: float
    outcome: DensityOutcome


@dataclass
class T109Certificate:
    status: T109Status
    extraction: CoherenceExtract
    uniform_positive: bool
    messages: list[str]


def _descendant_density(
    tree: CanonicalIntrusionTree,
    root: str,
    route: RouteLabel,
    n: int,
    resp: dict[str, dict[RouteLabel, float]],
) -> float:
    num = 0.0
    den = 0.0
    root_depth = cylinder_density(tree, root).depth if root in tree.nodes else 0

    def walk(nid: str) -> None:
        nonlocal num, den
        if nid not in tree.nodes:
            return
        d = cylinder_density(tree, nid).depth - root_depth
        phi = cylinder_density(tree, nid).phi_v
        den += phi
        w = resp.get(nid, {}).get(route, 0.0)
        if d == n:
            num += w * phi
        for c in tree.nodes[nid].child_ids:
            walk(c)

    if root in tree.nodes:
        walk(root)
    return num / den if den > 1e-12 else 0.0


def certify_t109(tree: CanonicalIntrusionTree) -> T109Certificate:
    mass = audit_route_signature_mass(tree)
    t091 = certify_t091(tree)
    system = audit_route_label_system(tree)
    resp = {r.node_id: r.weights for r in audit_route_responsibility(tree).records}
    route = mass.pigeonhole_route or "R_POSITIVE_SCALE"
    min_frac = 1.0 / max(len(system.node_sets[0].labels), 1) if system.node_sets else 0.0
    root = tree.root_id
    d1 = _descendant_density(tree, root, route, 1, resp)
    d2 = _descendant_density(tree, root, route, 2, resp) if tree.depth >= 2 else d1
    uniform = mass.pigeonhole_fraction >= min_frac and d1 > 0.05 and d2 > 0.05
    extract: CoherenceExtract = "NONE"
    if uniform and t091.mu_plus_positive:
        extract = "COHERENT_SUBSYSTEM"
    elif mass.pigeonhole_fraction >= min_frac:
        extract = "BUSHY_MEASURE"
    elif d1 < 0.01:
        extract = "ROUTE_OSCILLATION"
    else:
        extract = "CONCENTRATED_DESCENDANT"
    proved = extract in ("COHERENT_SUBSYSTEM", "BUSHY_MEASURE", "FINITE_CENTER_SPLIT")
    status: T109Status = "PROVED_LOCALLY" if proved else "CONJECTURAL_SELECTION_TARGET"
    return T109Certificate(status, extract, uniform, [f"route={route}, d1={d1:.3f}, extract={extract}"])
