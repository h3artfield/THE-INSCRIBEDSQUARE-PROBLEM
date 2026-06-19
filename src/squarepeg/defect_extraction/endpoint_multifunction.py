"""Compact-valued endpoint multifunction Phi (Directive 046)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_tree_boundary import TreeEndClass, build_tree_boundary

NestingClass = Literal[
    "END_HULLS_NESTED",
    "END_HULLS_NESTED_AFTER_FILLING",
    "END_HULLS_ONLY_EVENTUALLY_NESTED",
    "END_HULLS_NOT_NESTED",
]

EndpointDiameterClass = Literal[
    "SINGLETON_END",
    "ZERO_DIAMETER_END",
    "CONTINUUM_END",
    "POSITIVE_DIAMETER_END",
    "NONCONNECTED_ENDPOINT_SET",
]


@dataclass
class CompactSet2D:
    """Proxy for nonempty compact K subset of R^2: center + radius (Jordan disk)."""
    center: tuple[float, float]
    radius: float

    @property
    def diameter(self) -> float:
        return 2.0 * self.radius

    def contains(self, other: "CompactSet2D") -> bool:
        dx = self.center[0] - other.center[0]
        dy = self.center[1] - other.center[1]
        dist = math.hypot(dx, dy)
        return dist + other.radius <= self.radius + 1e-9


@dataclass
class EndHullRecord:
    end_id: str
    K_sets: list[CompactSet2D]
    nesting: NestingClass
    Phi: CompactSet2D
    d_phi: float
    d_infty: float
    diameter_class: EndpointDiameterClass
    singleton_point: tuple[float, float] | None


@dataclass
class EndpointMultifunctionAudit:
    records: list[EndHullRecord]
    nested_ae: bool
    singleton_mass_fraction: float
    continuum_mass_fraction: float
    messages: list[str]


def hull_from_node(tree: CanonicalIntrusionTree, nid: str) -> CompactSet2D:
    node = tree.nodes[nid]
    return CompactSet2D(node.center, max(node.diameter, 1e-6) / 2.0)


def intersect_disks(a: CompactSet2D, b: CompactSet2D) -> CompactSet2D | None:
    dx = b.center[0] - a.center[0]
    dy = b.center[1] - a.center[1]
    dist = math.hypot(dx, dy)
    if dist > a.radius + b.radius + 1e-9:
        return None
    if dist + min(a.radius, b.radius) <= max(a.radius, b.radius) + 1e-9:
        smaller = a if a.radius <= b.radius else b
        return CompactSet2D(smaller.center, smaller.radius)
    r_int = (a.radius + b.radius - dist) / 2.0
    t = (a.radius - b.radius + dist) / (2 * dist) if dist > 1e-12 else 0.5
    cx = a.center[0] + t * dx
    cy = a.center[1] + t * dy
    return CompactSet2D((cx, cy), max(r_int, 1e-9))


def _audit_nesting(K_sets: list[CompactSet2D]) -> NestingClass:
    if len(K_sets) < 2:
        return "END_HULLS_NESTED"
    nested = all(K_sets[j].contains(K_sets[j + 1]) for j in range(len(K_sets) - 1))
    if nested:
        return "END_HULLS_NESTED"
    eventual = False
    for start in range(len(K_sets)):
        if all(K_sets[j].contains(K_sets[j + 1]) for j in range(start, len(K_sets) - 1)):
            eventual = True
            break
    if eventual:
        return "END_HULLS_ONLY_EVENTUALLY_NESTED"
    if K_sets and all(
        math.hypot(k.center[0] - K_sets[-1].center[0], k.center[1] - K_sets[-1].center[1]) <= K_sets[-1].radius + 1e-6
        for k in K_sets
    ):
        return "END_HULLS_NESTED_AFTER_FILLING"
    return "END_HULLS_NOT_NESTED"


def endpoint_phi(K_sets: list[CompactSet2D]) -> CompactSet2D:
    if not K_sets:
        return CompactSet2D((0.5, 0.5), 0.0)
    cur = K_sets[0]
    for k in K_sets[1:]:
        nxt = intersect_disks(cur, k)
        if nxt is None:
            return cur
        cur = nxt
    return cur


def audit_endpoint_multifunction(tree: CanonicalIntrusionTree) -> EndpointMultifunctionAudit:
    ends = build_tree_boundary(tree)
    records: list[EndHullRecord] = []
    singleton_count = 0
    continuum_count = 0
    for end in ends:
        prefix = [n for n in end.ray_prefix if n in tree.nodes]
        K_sets = [hull_from_node(tree, n) for n in prefix] if prefix else []
        if not K_sets and end.spatial_center:
            K_sets = [CompactSet2D(end.spatial_center, 0.01)]
        nesting = _audit_nesting(K_sets)
        Phi = endpoint_phi(K_sets) if K_sets else CompactSet2D((0.5, 0.5), 0.0)
        d_inf = K_sets[-1].diameter if K_sets else 0.0
        d_phi = Phi.diameter
        dc: EndpointDiameterClass = "SINGLETON_END"
        pt: tuple[float, float] | None = None
        if d_phi <= 1e-6:
            dc = "ZERO_DIAMETER_END"
            pt = Phi.center
            singleton_count += 1
        elif d_phi < 0.02:
            dc = "SINGLETON_END"
            pt = Phi.center
            singleton_count += 1
        elif d_inf > 0.05 and d_phi > 0.05:
            dc = "POSITIVE_DIAMETER_END"
            continuum_count += 1
        else:
            dc = "CONTINUUM_END"
            continuum_count += 1
        records.append(EndHullRecord(end.end_id, K_sets, nesting, Phi, d_phi, d_inf, dc, pt))

    n = len(records) or 1
    nested_ae = sum(1 for r in records if r.nesting in ("END_HULLS_NESTED", "END_HULLS_NESTED_AFTER_FILLING")) >= 0.7 * n
    return EndpointMultifunctionAudit(
        records=records,
        nested_ae=nested_ae,
        singleton_mass_fraction=singleton_count / n,
        continuum_mass_fraction=continuum_count / n,
        messages=[f"records={len(records)}, singleton_frac={singleton_count/n:.2f}"],
    )
