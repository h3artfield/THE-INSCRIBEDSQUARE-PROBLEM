"""Cantor corona decomposition — good/neutral/bad nodes (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.signature_excess import audit_signature_excess

NodeClass = Literal["CONTRACTING", "NEUTRAL", "BAD"]
BadRoute = Literal[
    "CONCENTRATION",
    "FINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "POSITIVE_SCALE",
    "INFINITE_CENTER",
    "LARGE_CROSS_CHILD",
    "SIGN_CANCELLATION",
    "NONE",
]


@dataclass
class NodeClassification:
    node_id: str
    node_class: NodeClass
    P_over_Phi: float
    bad_route: BadRoute


@dataclass
class NeutralCorona:
    corona_id: int
    root_id: str
    node_ids: list[str]
    depth: int


@dataclass
class CantorCoronaAudit:
    classifications: list[NodeClassification]
    coronas: list[NeutralCorona]
    contracting_fraction: float
    neutral_fraction: float
    bad_fraction: float
    canonical: bool
    messages: list[str]


def _depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def audit_cantor_corona(tree: CanonicalIntrusionTree, *, epsilon: float = 0.08) -> CantorCoronaAudit:
    excess = audit_signature_excess(tree)
    inc = audit_incidence_concentration(tree)
    t091 = certify_t091(tree)
    classifications: list[NodeClassification] = []
    neutral_nodes: set[str] = set()

    for er in excess.records:
        ratio = er.P_v / er.Phi_v if er.Phi_v > 1e-12 else 0.0
        nc: NodeClass = "NEUTRAL"
        route: BadRoute = "NONE"
        if ratio <= 1.0 - epsilon:
            nc = "CONTRACTING"
        elif ratio <= 1.0 + epsilon:
            nc = "NEUTRAL"
            neutral_nodes.add(er.node_id)
        else:
            nc = "BAD"
            if inc.concentration_class == "CONCENTRATED":
                route = "CONCENTRATION"
            elif inc.concentration_class == "FINITE_CENTER":
                route = "FINITE_CENTER"
            elif "SIGN_CANCELLATION_EXCESS" in er.mechanisms:
                route = "SIGN_CANCELLATION"
            elif "CROSS_CHILD_WEDGE_EXCESS" in er.mechanisms:
                route = "LARGE_CROSS_CHILD"
            elif t091.mu_plus_positive:
                route = "POSITIVE_SCALE"
            elif not tree.nodes[er.node_id].jordan_hull:
                route = "NON_JORDAN"
            else:
                route = "INFINITE_CENTER"
        classifications.append(NodeClassification(er.node_id, nc, ratio, route))

    coronas: list[NeutralCorona] = []
    visited: set[str] = set()
    cid = 0
    for nid in sorted(neutral_nodes, key=lambda x: _depth(tree, x)):
        if nid in visited:
            continue
        corona_nodes = [nid]
        visited.add(nid)
        for cid2 in tree.nodes[nid].child_ids:
            if cid2 in neutral_nodes and cid2 not in visited:
                corona_nodes.append(cid2)
                visited.add(cid2)
        coronas.append(NeutralCorona(cid, nid, corona_nodes, len(corona_nodes)))
        cid += 1

    total = len(classifications) or 1
    contracting = sum(1 for c in classifications if c.node_class == "CONTRACTING") / total
    neutral = sum(1 for c in classifications if c.node_class == "NEUTRAL") / total
    bad = sum(1 for c in classifications if c.node_class == "BAD") / total

    return CantorCoronaAudit(
        classifications=classifications,
        coronas=coronas,
        contracting_fraction=contracting,
        neutral_fraction=neutral,
        bad_fraction=bad,
        canonical=True,
        messages=[f"contract={contracting:.2f}, neutral={neutral:.2f}, bad={bad:.2f}, coronas={len(coronas)}"],
    )
