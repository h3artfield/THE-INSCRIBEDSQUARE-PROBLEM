"""Nonsummable intrusion ray measures and falsification models (Directive 043)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode
from squarepeg.defect_extraction.intrinsic_tree_nonsummability import N_ray
from squarepeg.defect_extraction.intrusion_ray_geometry import IntrusionRay, extract_ray
from squarepeg.defect_extraction.summable_ray_signature import audit_summable_ray_signature, ray_scale_mass


@dataclass
class NonsummableRayMeasure:
    ray: IntrusionRay
    S_ray: float
    S_area: float
    intrinsic_tail: float
    N_ray: float
    summable: bool
    plateau_run: bool


@dataclass
class NonsummableRayMeasureAudit:
    measure: NonsummableRayMeasure | None
    messages: list[str]


def build_harmonic_nonsummable_ray(*, length: int = 16) -> CanonicalIntrusionTree:
    """Harmonic-scale ray: r_j ~ 1/j, sum r_j diverges."""
    nodes: dict[str, IntrusionTreeNode] = {}
    prev: str | None = None
    for j in range(length):
        r = 1.0 / (j + 1)
        nid = f"h{j}"
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(j / length, (j + 1) / length),
            diameter=r,
            defect=0.08 * r,
            gate_count=2,
            center=(0.5, 0.5),
            sign=1 if j % 2 == 0 else -1,
            parent_id=prev,
            child_ids=[],
            jordan_hull=True,
        )
        if prev:
            nodes[prev].child_ids.append(nid)
        prev = nid
    return CanonicalIntrusionTree(
        root_id="h0",
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=length - 1,
    )


def build_plateau_ray(*, length: int = 14, plateau_len: int = 6) -> CanonicalIntrusionTree:
    """Plateau ray: r_{j+1}/r_j -> 1 on a long run; nonsummable scale mass."""
    nodes: dict[str, IntrusionTreeNode] = {}
    prev: str | None = None
    r = 1.0
    for j in range(length):
        if j >= length - plateau_len:
            r *= 0.999
        else:
            r *= 0.55
        nid = f"p{j}"
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(j / length, (j + 1) / length),
            diameter=r,
            defect=0.12 * r,
            gate_count=2 + (j % 3),
            center=(0.5 + 0.02 * math.sin(j), 0.5),
            sign=1,
            parent_id=prev,
            child_ids=[],
            jordan_hull=True,
        )
        if prev:
            nodes[prev].child_ids.append(nid)
        prev = nid
    return CanonicalIntrusionTree(
        root_id="p0",
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=length - 1,
    )


def build_moving_center_ray(*, length: int = 12) -> CanonicalIntrusionTree:
    """Nonsummable ray with moving centers."""
    nodes: dict[str, IntrusionTreeNode] = {}
    prev: str | None = None
    r = 1.0
    for j in range(length):
        angle = 2 * math.pi * j / length
        nid = f"m{j}"
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(j / length, (j + 1) / length),
            diameter=r,
            defect=0.07 * r,
            gate_count=3,
            center=(0.5 + 0.3 * math.cos(angle), 0.5 + 0.3 * math.sin(angle)),
            sign=(-1) ** j,
            parent_id=prev,
            child_ids=[],
            jordan_hull=True,
        )
        if prev:
            nodes[prev].child_ids.append(nid)
        prev = nid
        r *= 0.88
    return CanonicalIntrusionTree(
        root_id="m0",
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=length - 1,
    )


def build_pinched_end_ray(*, length: int = 10) -> CanonicalIntrusionTree:
    """Ray with pinched end hull (non-Jordan flag on terminal node)."""
    tree = build_plateau_ray(length=length, plateau_len=4)
    last = list(tree.nodes.keys())[-1]
    tree.nodes[last].jordan_hull = False
    return tree


def audit_nonsummable_ray_measure(tree: CanonicalIntrusionTree) -> NonsummableRayMeasureAudit:
    ray = extract_ray(tree)
    if not ray:
        return NonsummableRayMeasureAudit(None, ["no ray"])
    mass = ray_scale_mass(ray)
    nr = N_ray(ray)
    sig = audit_summable_ray_signature(tree)
    radii = [d.diameter for d in ray.data]
    ratios = [radii[i + 1] / max(radii[i], 1e-9) for i in range(len(radii) - 1)] if len(radii) > 1 else []
    plateau = len(ratios) >= 4 and all(0.95 <= r <= 1.05 for r in ratios[-4:])
    summable = sig is not None and sig.satisfies_summable
    if plateau and mass.S_ray > 1.8:
        summable = False
    if mass.S_ray > 3.5:
        summable = False
    if nr >= 0.05:
        summable = summable and nr < 0.05
    measure = NonsummableRayMeasure(
        ray=ray,
        S_ray=mass.S_ray,
        S_area=mass.S_area,
        intrinsic_tail=nr * (sum(d.defect for d in ray.data) or 1.0),
        N_ray=nr,
        summable=summable,
        plateau_run=plateau,
    )
    return NonsummableRayMeasureAudit(
        measure=measure,
        messages=[f"S_ray={mass.S_ray:.3f}, summable={summable}, plateau={plateau}"],
    )
