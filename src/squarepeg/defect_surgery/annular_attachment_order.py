"""Gate-order compatibility for annular attachment chains (Directive 026)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Literal

from squarepeg.defect_surgery.packet_disk import PacketDisk, Point

PreliminaryAnnularVerdict = Literal[
    "CURRENT_ANNULAR_CLASS_SUFFICIENT",
    "CURRENT_ANNULAR_CLASS_INSUFFICIENT",
    "CURRENT_ANNULAR_CLASS_UNRESOLVED",
]


class AttachmentVertexKind(str, Enum):
    RETAINED_TO_CHORD = "RETAINED_TO_CHORD"
    CHORD_TO_RETAINED = "CHORD_TO_RETAINED"
    RETAINED_ENDPOINT = "RETAINED_ENDPOINT"
    PARAMETER_SEAM = "PARAMETER_SEAM"


@dataclass(frozen=True)
class GatePair:
    interval_start: int
    interval_end: int
    point_a: Point
    point_b: Point
    center: Point
    radius: float

    @property
    def lo(self) -> int:
        return min(self.interval_start, self.interval_end)

    @property
    def hi(self) -> int:
        return max(self.interval_start, self.interval_end)


def gate_from_disk(d: PacketDisk, vertices: list[Point], center: Point | None = None) -> GatePair:
    c = center or d.center
    return GatePair(
        interval_start=d.interval_start,
        interval_end=d.interval_end,
        point_a=vertices[d.interval_start],
        point_b=vertices[d.interval_end],
        center=c,
        radius=d.radius,
    )


def _projection_scalar(p: Point, axis: Point) -> float:
    return p[0] * axis[0] + p[1] * axis[1]


def endpoints_interleave(g1: GatePair, g2: GatePair) -> bool:
    """Forbidden pattern A_i, A_j, B_i, B_j on a common projection axis."""
    pts = [g1.point_a, g1.point_b, g2.point_a, g2.point_b]
    ax = (pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
    if ax[0] ** 2 + ax[1] ** 2 < 1e-12:
        ax = (1.0, 0.0)
    labels = ["A1", "B1", "A2", "B2"]
    order = [lb for _, lb in sorted(zip([_projection_scalar(p, ax) for p in pts], labels))]
    forbidden = (["A1", "A2", "B1", "B2"], ["A1", "A2", "B2", "B1"], ["A2", "A1", "B1", "B2"])
    reverse = [order[3], order[2], order[1], order[0]]
    return order in forbidden or reverse in forbidden


def is_gate_ordered(gates: list[GatePair]) -> bool:
    ordered = sorted(gates, key=lambda g: g.lo)
    for i in range(len(ordered)):
        for j in range(i + 1, len(ordered)):
            if endpoints_interleave(ordered[i], ordered[j]):
                return False
    return True


def classify_attachment_vertex(
    prev_kind: str | None,
    is_chord_endpoint: bool,
    at_seam: bool,
) -> AttachmentVertexKind:
    if at_seam:
        return AttachmentVertexKind.PARAMETER_SEAM
    if is_chord_endpoint and prev_kind == "retained":
        return AttachmentVertexKind.RETAINED_TO_CHORD
    if is_chord_endpoint and prev_kind == "chord":
        return AttachmentVertexKind.CHORD_TO_RETAINED
    return AttachmentVertexKind.RETAINED_ENDPOINT


def interleaving_gate_counterexample() -> list[GatePair]:
    c = (1.5, 0.0)
    g1 = GatePair(0, 1, (0.0, 0.0), (2.0, 0.0), c, 0.05)
    g2 = GatePair(2, 3, (1.0, 0.0), (3.0, 0.0), c, 0.05)
    return [g1, g2]


def ordered_gate_example(center: Point = (0.0, 0.0), n: int = 4) -> list[GatePair]:
    gates: list[GatePair] = []
    for k in range(n):
        th0 = math.pi / 4 + k * math.pi / (2 * n)
        th1 = th0 + math.pi / (4 * n)
        r = 0.04 - k * 0.008
        a = (r * math.cos(th0), r * math.sin(th0))
        b = (r * math.cos(th1), r * math.sin(th1))
        gates.append(GatePair(k * 2, k * 2 + 1, a, b, center, r * 0.12))
    return gates


def interleaving_attachment_components() -> list:
    from squarepeg.defect_surgery.exact_component_decomposition import PathComponent, component_delta

    return [
        PathComponent("crosscut", [(0.0, 0.0), (2.0, 0.0)], component_delta([(0.0, 0.0), (2.0, 0.0)])),
        PathComponent("retained", [(2.0, 0.0), (1.0, 0.0)], component_delta([(2.0, 0.0), (1.0, 0.0)])),
        PathComponent("crosscut", [(1.0, 0.0), (1.0, 1.0)], component_delta([(1.0, 0.0), (1.0, 1.0)])),
    ]


def current_annular_class_verdict() -> PreliminaryAnnularVerdict:
    gates = interleaving_gate_counterexample()
    if not is_gate_ordered(gates):
        return "CURRENT_ANNULAR_CLASS_INSUFFICIENT"
    return "CURRENT_ANNULAR_CLASS_UNRESOLVED"
