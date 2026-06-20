"""Coherent route subtree selection — T103 (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.multigeneration_packing import certify_t093
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.route_label_measure import audit_route_label_measure

T103Status = Literal["CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY"]
SubtreeType = Literal[
    "ROUTED_RAY",
    "ROUTED_FINITE_BRANCH_SUBTREE",
    "ROUTED_BUSHY_SUBTREE",
    "ROUTED_MEASURE_SUBTREE",
    "ROUTE_OSCILLATION",
    "NONE",
]


@dataclass
class CoherentSubtreeRecord:
    root_id: str
    subtree_type: SubtreeType
    depth: int
    signature_coverage: float
    uniform_route: str
    ancestry_coherent: bool


@dataclass
class CoherentRouteSubtreeAudit:
    subtrees: list[CoherentSubtreeRecord]
    positive_signature_subsystem: bool
    uniform_constants: bool
    messages: list[str]


@dataclass
class T103Certificate:
    status: T103Status
    coherent_subsystem_exists: bool
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


def audit_coherent_route_subtree(tree: CanonicalIntrusionTree) -> CoherentRouteSubtreeAudit:
    corona = audit_cantor_corona(tree)
    routes = audit_route_label_measure(tree)
    subtrees: list[CoherentSubtreeRecord] = []
    total_phi = sum(cylinder_density(tree, n).phi_v for n in tree.nodes if tree.nodes[n].child_ids) or 1.0
    for c in corona.coronas:
        depth = _subtree_depth(tree, c.root_id)
        phi = cylinder_density(tree, c.root_id).phi_v if c.root_id in tree.nodes else 0.0
        cov = phi / total_phi
        cc = len(tree.nodes[c.root_id].child_ids) if c.root_id in tree.nodes else 0
        st: SubtreeType = "NONE"
        if routes.persistent_fraction >= 0.5 and depth >= 1:
            if cc == 1:
                st = "ROUTED_RAY"
            elif cc >= 2:
                st = "ROUTED_BUSHY_SUBTREE"
            else:
                st = "ROUTED_FINITE_BRANCH_SUBTREE"
        elif routes.persistent_fraction < 0.5:
            st = "ROUTE_OSCILLATION"
        subtrees.append(
            CoherentSubtreeRecord(
                c.root_id,
                st,
                depth,
                cov,
                routes.dominant_label or "UNKNOWN",
                st != "ROUTE_OSCILLATION" and st != "NONE",
            )
        )
    pos = any(s.ancestry_coherent and s.signature_coverage > 0.01 for s in subtrees)
    uniform = routes.persistent_fraction >= 0.75
    return CoherentRouteSubtreeAudit(
        subtrees=subtrees,
        positive_signature_subsystem=pos,
        uniform_constants=uniform,
        messages=[f"subtrees={len(subtrees)}, pos={pos}"],
    )


def certify_t103(tree: CanonicalIntrusionTree) -> T103Certificate:
    audit = audit_coherent_route_subtree(tree)
    t093 = certify_t093(tree)
    # Universal coherence requires uniform route constants on a deep subsystem, not fixture homogeneity alone.
    deep = any(s.depth >= 2 and s.ancestry_coherent for s in audit.subtrees)
    proved = audit.positive_signature_subsystem and audit.uniform_constants and deep
    if not proved and t093.status == "PROVED_LOCALLY":
        proved = False
    status: T103Status = "PROVED_LOCALLY" if proved else "CONJECTURAL_SELECTION_TARGET"
    return T103Certificate(status, audit.positive_signature_subsystem, audit.messages)
