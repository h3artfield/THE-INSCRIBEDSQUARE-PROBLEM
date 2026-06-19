"""Intrusion graph for dirty lobes (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_surgery.annular_attachment_order import endpoints_interleave, GatePair

InterleavingKind = Literal[
    "BOUNDARY_INTERLEAVE",
    "PARAMETER_INTERLEAVE",
    "GATE_INTERLEAVE",
    "SPATIAL_OVERLAP_ONLY",
    "NONE",
]


@dataclass
class IntrusionEdge:
    lobe_id: str
    entry: tuple[float, float]
    exit: tuple[float, float]
    via_chord: bool


@dataclass
class IntrusionGraph:
    lobe_ids: list[str]
    edges: list[IntrusionEdge]
    interleaving: InterleavingKind


def classify_interleaving(g1: GatePair, g2: GatePair) -> InterleavingKind:
    if endpoints_interleave(g1, g2):
        return "GATE_INTERLEAVE"
    return "NONE"


def build_intrusion_graph(
    lobe_ids: list[str],
    gates: list[GatePair] | None = None,
) -> IntrusionGraph:
    edges: list[IntrusionEdge] = []
    kind: InterleavingKind = "NONE"
    if gates and len(gates) >= 2:
        for i in range(len(gates) - 1):
            k = classify_interleaving(gates[i], gates[i + 1])
            if k != "NONE":
                kind = k
    return IntrusionGraph(lobe_ids=lobe_ids, edges=edges, interleaving=kind)
