"""Infinite-center critical geometry (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

CenterGrowth = Literal[
    "POLYNOMIAL",
    "EXPONENTIAL",
    "DIFFUSE",
    "SPATIALLY_PACKED",
    "PARAMETER_CORRELATED",
    "BOUNDED",
]

InfiniteCenterRoute = Literal[
    "QUADRATIC_PACKING_T087",
    "DIFFUSE_INCIDENCE",
    "PARAMETER_DISCONNECTED",
    "POSITIVE_SCALE_NONANNULAR",
    "NON_JORDAN",
    "CRITICAL_RESIDUAL",
]


@dataclass
class CenterGrowthRecord:
    node_id: str
    N_c: int
    growth: CenterGrowth
    route: InfiniteCenterRoute


@dataclass
class InfiniteCenterCriticalAudit:
    records: list[CenterGrowthRecord]
    max_centers: int
    unbounded: bool
    dominant_route: InfiniteCenterRoute
    messages: list[str]


def N_c(tree: CanonicalIntrusionTree, node_id: str, *, K: int = 4) -> int:
    node = tree.nodes[node_id]
    if not node.child_ids:
        return 1
    buckets: dict[tuple[int, int], float] = {}
    for cid in node.child_ids:
        if cid not in tree.nodes:
            continue
        c = tree.nodes[cid].center
        key = (round(c[0] * K), round(c[1] * K))
        buckets[key] = buckets.get(key, 0.0) + cylinder_density(tree, cid).m_v
    return len(buckets)


def audit_infinite_center_critical(tree: CanonicalIntrusionTree, *, K: int = 4) -> InfiniteCenterCriticalAudit:
    records: list[CenterGrowthRecord] = []
    max_nc = 0
    depths_nc: list[tuple[int, int]] = []

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        nc = N_c(tree, nid, K=K)
        max_nc = max(max_nc, nc)
        d = 0
        cur = node
        while cur.parent_id:
            d += 1
            cur = tree.nodes[cur.parent_id]
        depths_nc.append((d, nc))

    growth: CenterGrowth = "BOUNDED"
    if max_nc <= K + 1:
        growth = "BOUNDED"
    elif depths_nc and max_nc > 2 * K:
        growth = "EXPONENTIAL" if any(nc > 3 * K for _, nc in depths_nc) else "POLYNOMIAL"
    else:
        growth = "DIFFUSE"

    route: InfiniteCenterRoute = "CRITICAL_RESIDUAL"
    if growth == "BOUNDED":
        route = "QUADRATIC_PACKING_T087"
    elif growth == "POLYNOMIAL":
        route = "DIFFUSE_INCIDENCE"
    elif growth == "EXPONENTIAL":
        route = "POSITIVE_SCALE_NONANNULAR"
    elif not all(n.jordan_hull for n in tree.nodes.values()):
        route = "NON_JORDAN"

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        nc = N_c(tree, nid, K=K)
        records.append(CenterGrowthRecord(nid, nc, growth, route))

    unbounded = growth != "BOUNDED"
    return InfiniteCenterCriticalAudit(
        records=records,
        max_centers=max_nc,
        unbounded=unbounded,
        dominant_route=route,
        messages=[f"max_Nc={max_nc}, growth={growth}, route={route}"],
    )
