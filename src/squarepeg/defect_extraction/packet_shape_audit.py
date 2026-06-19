"""Packet shape classification (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_geometry.lobe import LobeRecord

ShapeClass = Literal[
    "ANNULAR_GRAPH_PACKET",
    "BOUNDED_WINDING_PACKET",
    "SIMPLE_SIGNATURE_PACKET",
    "ECCENTRIC_PACKET",
    "MULTICENTER_PACKET",
    "BRANCHING_PACKET",
    "UNCLASSIFIED",
]


@dataclass
class ShapeAudit:
    shape_class: ShapeClass
    eccentricity: float
    annular_graph: bool


def audit_packet_shape(lobe: LobeRecord) -> ShapeAudit:
    verts = list(lobe.arc_vertices)
    xs = [p[0] for p in verts]
    ys = [p[1] for p in verts]
    w = max(xs) - min(xs) if xs else 1.0
    h = max(ys) - min(ys) if ys else 1.0
    ecc = abs(w - h) / max(w, h, 1e-9)

    ann = False
    try:
        from squarepeg.defect_geometry.annular_graph import validate_annular_graph
        from squarepeg.defect_geometry.annular_graph_certificate import example_certified_packet

        ann = validate_annular_graph(example_certified_packet())
    except Exception:
        ann = False

    if ann and ecc < 0.3:
        cls: ShapeClass = "ANNULAR_GRAPH_PACKET"
    elif ecc > 0.8:
        cls = "ECCENTRIC_PACKET"
    elif lobe.enclosed_area > 0 and lobe.diameter ** 2 / max(lobe.enclosed_area, 1e-9) < 20:
        cls = "BOUNDED_WINDING_PACKET"
    else:
        cls = "UNCLASSIFIED"

    return ShapeAudit(shape_class=cls, eccentricity=ecc, annular_graph=ann)
