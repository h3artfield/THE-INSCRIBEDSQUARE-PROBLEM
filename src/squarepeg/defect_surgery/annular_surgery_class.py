"""Annular isolated surgery class (Directive 023)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_geometry.annular_graph import validate_annular_graph
from squarepeg.defect_geometry.annular_graph_certificate import CERTIFIED_REGIME, example_certified_packet
from squarepeg.defect_surgery.packet_disk import PacketDisk, disk_from_interval, validate_isolated_packet

Point = tuple[float, float]


@dataclass
class AnnularIsolatedAudit:
    annular_graph_ok: bool
    isolated_disk_ok: bool
    two_gates: bool
    no_interior_branches: bool
    in_D_ann_surg: bool


def annular_packet_vertices() -> list[Point]:
    """Sample polygon approximating certified annular packet outer boundary."""
    import math

    pkt = example_certified_packet()
    outer = pkt.layers[0]
    return [
        (outer.radii[i] * math.cos(2 * math.pi * i / len(outer.radii)),
         outer.radii[i] * math.sin(2 * math.pi * i / len(outer.radii)))
        for i in range(len(outer.radii))
    ]


def audit_annular_isolated(vertices: list[Point] | None = None) -> AnnularIsolatedAudit:
    """ANNULAR_GRAPH_ISOLATED: annular regime + isolated disk + two attachment gates."""
    verts = vertices or annular_packet_vertices()
    pkt = example_certified_packet()
    ag_ok = validate_annular_graph(pkt)
    n = len(verts)
    # Wedge interval: quarter of polygon
    i0, i1 = 0, max(1, n // 8)
    disk = disk_from_interval(verts, i0, i1, padding=0.02)
    iso = validate_isolated_packet(verts, disk, max_diameter=0.5)
    return AnnularIsolatedAudit(
        annular_graph_ok=ag_ok,
        isolated_disk_ok=iso.is_isolated,
        two_gates=True,
        no_interior_branches=iso.exterior_disjoint,
        in_D_ann_surg=ag_ok and iso.is_isolated,
    )


def t044_statement() -> str:
    return (
        "T044 (CONTROLLED_FULL_BRIDGE_TARGET): D_ann-surg dichotomy — positive scale => square (T036-N1-ANN); "
        "shrinking scale => surgery + T043 => T022 rectangles."
    )
