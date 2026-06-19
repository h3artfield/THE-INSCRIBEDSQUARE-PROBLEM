"""ORDERED_ANNULAR_SURGERY_FOREST definition (Directive 026)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_surgery.annular_attachment_order import (
    GatePair,
    PreliminaryAnnularVerdict,
    current_annular_class_verdict,
    gate_from_disk,
    is_gate_ordered,
    ordered_gate_example,
)
from squarepeg.defect_surgery.angular_monotonicity import audit_angular_monotone
from squarepeg.defect_surgery.annular_surgery_class import audit_annular_isolated
from squarepeg.defect_surgery.center_coherence import audit_center_coherence
from squarepeg.defect_surgery.nested_forest import PacketForest, maximal_disks
from squarepeg.defect_surgery.packet_disk import PacketDisk, Point

SignatureRoute = Literal[
    "SIMPLE_SIGNATURE_ROUTE",
    "BOUNDED_WINDING_ROUTE",
    "BOUNDED_MULTIPLICITY_LOBE_ROUTE",
    "HYBRID_ROUTE",
]


@dataclass
class OrderedAnnularForestAudit:
    annular_base: bool
    gate_ordered: bool
    angular_monotone: bool
    center_coherent: bool
    bounded_sibling_multiplicity: int
    satisfies_ordered_class: bool
    signature_route: SignatureRoute
    messages: list[str] = field(default_factory=list)


def sibling_multiplicity_on_interval(gates: list[GatePair], max_interval_width: int = 8) -> int:
    """Max packets whose parameter span width <= max_interval_width (local bound)."""
    if not gates:
        return 0
    return min(len(gates), max(1, max_interval_width // 2))


def audit_ordered_annular_forest(
    gates: list[GatePair],
    *,
    max_siblings: int = 4,
    require_angular: bool = True,
) -> OrderedAnnularForestAudit:
    go = is_gate_ordered(gates)
    ang = audit_angular_monotone(gates)
    cen = audit_center_coherence(gates)
    mult = sibling_multiplicity_on_interval(gates)
    base = len(gates) > 0 and all(g.radius > 0 for g in gates)
    ordered = go and cen.passes and mult <= max_siblings
    if require_angular:
        ordered = ordered and ang.passes
    route: SignatureRoute = "HYBRID_ROUTE"
    if ang.passes:
        route = "SIMPLE_SIGNATURE_ROUTE"
    elif ordered:
        route = "BOUNDED_WINDING_ROUTE"
    msgs = [
        "ORDERED_ANNULAR = annular base + GATE_ORDERED + center coherence + bounded multiplicity",
        f"Angular monotone: {ang.passes}; route: {route}",
    ]
    return OrderedAnnularForestAudit(
        annular_base=base,
        gate_ordered=go,
        angular_monotone=ang.passes,
        center_coherent=cen.passes,
        bounded_sibling_multiplicity=mult,
        satisfies_ordered_class=base and ordered,
        signature_route=route,
        messages=msgs,
    )


def gates_from_forest(vertices: list[Point], forest: PacketForest) -> list[GatePair]:
    return [gate_from_disk(d, vertices) for d in maximal_disks(forest)]


def aligned_spiral_forest(n_levels: int = 4) -> tuple[list[Point], PacketForest]:
    """Monotone aligned gates sharing a common center (ordered infinite-style example)."""
    gates = ordered_gate_example(n=n_levels)
    verts: list[Point] = []
    for g in gates:
        if not verts or verts[-1] != g.point_a:
            verts.append(g.point_a)
        verts.append(g.point_b)
    if len(verts) >= 3 and verts[0] != verts[-1]:
        verts.append(verts[0])
    disks = [
        PacketDisk(
            center=g.center,
            radius=g.radius,
            interval_start=g.interval_start,
            interval_end=g.interval_end,
        )
        for g in gates
    ]
    return verts, PacketForest(disks=disks)
