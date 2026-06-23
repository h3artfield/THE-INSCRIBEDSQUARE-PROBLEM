"""Curve-level saturation hull geometry (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure

HullClass = Literal["JORDAN", "NON_JORDAN", "HARMLESS_QUOTIENT"]


@dataclass
class SaturationHull:
    hull_id: str
    jordan: bool
    boundary_count: int
    locally_connected: bool
    pinch_detected: bool
    collision_mass: float
    hull_class: HullClass
    curve_level: bool


@dataclass
class SaturationHullAudit:
    hulls: list[SaturationHull]
    curve_level: bool
    messages: list[str]


def audit_saturation_hulls(tree: CanonicalIntrusionTree) -> SaturationHullAudit:
    collision = audit_gate_collision_measure(tree)
    hulls: list[SaturationHull] = []
    for nid, node in tree.nodes.items():
        diag = 0.0
        for m in collision.measures:
            if m.parent_id == nid:
                diag = m.diagonal_mass
        pinch = node.diameter < 1e-4 and diag > 0
        jordan = node.jordan_hull
        hc: HullClass = "JORDAN" if jordan else "NON_JORDAN"
        if jordan and diag > 0:
            hc = "HARMLESS_QUOTIENT"
        hulls.append(
            SaturationHull(
                nid,
                jordan,
                max(len(node.child_ids), 1),
                True,
                pinch,
                diag,
                hc,
                True,
            )
        )
    return SaturationHullAudit(hulls=hulls, curve_level=True, messages=[f"n={len(hulls)}"])
