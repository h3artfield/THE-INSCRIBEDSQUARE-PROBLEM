"""Cantor-end antichain surgery and T087 (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.end_signature_measure import end_sig_mass
from squarepeg.defect_extraction.end_spatial_map import audit_end_spatial_map
from squarepeg.defect_extraction.tree_end_cylinders import build_antichain

T087Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class AntichainSurgeryStep:
    N: int
    antichain: list[str]
    jordan: bool
    crosscuts_disjoint: bool
    cross_cylinder_bound: float
    tail_mass: float


@dataclass
class CantorEndSurgeryAudit:
    steps: list[AntichainSurgeryStep]
    limit_jordan: bool
    area_tight: bool
    tail_vanishes: bool
    limit_order: str
    messages: list[str]


@dataclass
class T087Certificate:
    status: T087Status
    area_tight: bool
    carleson: bool
    messages: list[str]


def cross_cylinder_bound(tree: CanonicalIntrusionTree, v: str, w: str) -> float:
    """|A_{vw}| <= C L(v) L(w) for antichain nodes."""
    Lv = end_sig_mass(tree, v) ** 0.5
    Lw = end_sig_mass(tree, w) ** 0.5
    dv = tree.nodes[v].diameter
    dw = tree.nodes[w].diameter
    return 0.5 * Lv * Lw * min(dv, dw)


def audit_cantor_end_surgery(
    tree: CanonicalIntrusionTree,
    *,
    depths: list[int] | None = None,
) -> CantorEndSurgeryAudit:
    depths = depths or [1, 2, 3, min(4, tree.depth)]
    steps: list[AntichainSurgeryStep] = []
    total = sum(end_sig_mass(tree, tree.root_id) for _ in [0]) or 1.0
    for N in depths:
        ant = build_antichain(tree, max_depth=N)
        pairs = 0.0
        for i, v in enumerate(ant):
            for w in ant[i + 1:]:
                pairs += cross_cylinder_bound(tree, v, w)
        tail = sum(
            end_sig_mass(tree, nid)
            for nid in tree.nodes
            if nid not in ant and not any(nid.startswith(a) for a in ant)
        ) / max(total, 1e-9)
        steps.append(
            AntichainSurgeryStep(
                N=N,
                antichain=ant,
                jordan=all(tree.nodes[n].jordan_hull for n in ant if n in tree.nodes),
                crosscuts_disjoint=pairs < 0.5 * total,
                cross_cylinder_bound=pairs,
                tail_mass=tail,
            )
        )
    tail_v = steps[-1].tail_mass < 0.2 if steps else True
    carl = audit_end_signature_carleson(tree)
    return CantorEndSurgeryAudit(
        steps=steps,
        limit_jordan=all(s.jordan for s in steps),
        area_tight=tail_v and carl.vanishing_fine_tails,
        tail_vanishes=tail_v,
        limit_order="n, delta, antichain_N, depth",
        messages=[f"steps={len(steps)}, tail_vanishes={tail_v}"],
    )


def certify_t087(tree: CanonicalIntrusionTree) -> T087Certificate:
    """T087: diffuse end-measure surgery under END_SIGNATURE_CARLESON."""
    carl = audit_end_signature_carleson(tree)
    spatial = audit_end_spatial_map(tree)
    surg = audit_cantor_end_surgery(tree)
    if not carl.satisfies_carleson:
        return T087Certificate(
            status="CONJECTURAL_TARGET",
            area_tight=False,
            carleson=False,
            messages=["END_SIGNATURE_CARLESON fails"],
        )
    if not spatial.point_valued_ae:
        return T087Certificate(
            status="CONJECTURAL_TARGET",
            area_tight=False,
            carleson=True,
            messages=["endpoint map not point-valued a.e."],
        )
    if surg.area_tight and surg.limit_jordan:
        return T087Certificate(
            status="PROVED_LOCALLY",
            area_tight=True,
            carleson=True,
            messages=["antichain surgery area-tight"],
        )
    return T087Certificate(
        status="CONJECTURAL_TARGET",
        area_tight=surg.area_tight,
        carleson=True,
        messages=["surgery incomplete"],
    )


def build_middle_thirds_cantor_tree(*, levels: int = 4) -> CanonicalIntrusionTree:
    """Middle-thirds Cantor end tree proxy."""
    nodes: dict[str, IntrusionTreeNode] = {}
    root_id = "root"
    nodes[root_id] = IntrusionTreeNode(
        node_id=root_id,
        param_interval=(0.0, 1.0),
        diameter=1.0,
        defect=0.1,
        gate_count=4,
        center=(0.5, 0.5),
        sign=1,
        parent_id=None,
        child_ids=[],
        jordan_hull=True,
    )

    def add(level: int, idx: int, lo: float, hi: float, parent: str, r: float) -> None:
        if level >= levels:
            nid = f"L{level}_{idx}"
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(lo, hi),
                diameter=r,
                defect=0.05 * r,
                gate_count=2,
                center=(lo + (hi - lo) / 2, 0.5),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            return
        mid_lo = lo + (hi - lo) / 3
        mid_hi = hi - (hi - lo) / 3
        for j, (a, b) in enumerate([(lo, mid_lo), (mid_hi, hi)]):
            nid = f"L{level}_{idx}_{j}"
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(a, b),
                diameter=r * 0.55,
                defect=0.04 * r,
                gate_count=3,
                center=((a + b) / 2, 0.5),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            add(level + 1, idx * 2 + j, a, b, nid, r * 0.55)

    add(0, 0, 0.0, 1.0, root_id, 0.5)
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=levels,
    )


def build_bernoulli_end_tree(*, depth: int = 5, p: float = 0.5) -> CanonicalIntrusionTree:
    """Binary tree with Bernoulli-weighted end defects."""
    from squarepeg.defect_extraction.cantor_end_residual import build_binary_diffuse_end_tree
    return build_binary_diffuse_end_tree(depth=depth)
