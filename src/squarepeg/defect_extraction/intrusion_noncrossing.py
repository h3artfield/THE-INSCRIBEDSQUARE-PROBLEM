"""Planar noncrossing structure for intrusion arcs (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Point = tuple[float, float]

EndpointOrder = Literal["NESTED", "SEPARATED", "INTERLEAVING", "INVALID"]


@dataclass
class IntrusionComponent:
    """Connected intrusion K with parameter interval I_K."""

    component_id: str
    param_interval: tuple[float, float]
    entry: Point
    exit: Point
    via_chord_entry: bool
    via_chord_exit: bool
    children: list[str]


@dataclass
class NoncrossingAudit:
    endpoint_order: EndpointOrder
    compatible: bool
    planar_graph_edges: list[tuple[str, str]]


def _projection_order(labels: list[tuple[str, Point]], axis: Point) -> list[str]:
    ax, ay = axis
    keyed = sorted(
        [(p[0] * ax + p[1] * ay, lb) for lb, p in labels],
        key=lambda x: x[0],
    )
    return [lb for _, lb in keyed]


def classify_endpoint_order(a1: Point, b1: Point, a2: Point, b2: Point) -> EndpointOrder:
    """Cyclic endpoint order for two disjoint intrusion components."""
    ax = (b1[0] - a1[0], b1[1] - a1[1])
    if ax[0] ** 2 + ax[1] ** 2 < 1e-12:
        ax = (1.0, 0.0)

    def proj(p: Point) -> float:
        return p[0] * ax[0] + p[1] * ax[1]

    labels = [("A1", proj(a1)), ("B1", proj(b1)), ("A2", proj(a2)), ("B2", proj(b2))]
    order = [lb for lb, _ in sorted(labels, key=lambda x: x[1])]
    forbidden = (["A1", "A2", "B1", "B2"], ["A2", "A1", "B2", "B1"], ["A2", "A1", "B1", "B2"], ["B2", "B1", "A1", "A2"])
    reverse = [order[3], order[2], order[1], order[0]]
    if order in forbidden or reverse in forbidden:
        return "INTERLEAVING"
    t1, t2 = sorted((proj(a2), proj(b2)))
    lo, hi = sorted((proj(a1), proj(b1)))
    if t1 >= lo and t2 <= hi:
        return "NESTED"
    if t2 <= lo or t1 >= hi:
        return "SEPARATED"
    return "NESTED"


def audit_noncrossing(components: list[IntrusionComponent]) -> NoncrossingAudit:
    """
    Disjoint embedded arcs in a Jordan disk admit noninterleaving endpoint orders
    (nested or separated) on a common projection axis.
    """
    if len(components) < 2:
        return NoncrossingAudit("SEPARATED", True, [])
    c1, c2 = components[0], components[1]
    order = classify_endpoint_order(c1.entry, c1.exit, c2.entry, c2.exit)
    compatible = order in ("NESTED", "SEPARATED")
    edges = [(c1.component_id, c2.component_id)] if compatible else []
    return NoncrossingAudit(endpoint_order=order, compatible=compatible, planar_graph_edges=edges)
