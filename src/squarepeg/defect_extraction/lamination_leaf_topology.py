"""Leaf topology classification (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

LeafClass = Literal[
    "JORDAN_LEAF",
    "PINCHED_LEAF",
    "MULTIBOUNDARY_LEAF",
    "DENDRITIC_LEAF",
    "NONLOCALLY_CONNECTED_LEAF",
]

GateLeafClass = Literal[
    "TWO_GATE_LEAF",
    "FINITE_MULTIGATE_LEAF",
    "INFINITE_GATE_ACCUMULATION",
    "NO_CANONICAL_GATE",
]


@dataclass
class LeafTopologyAudit:
    leaf_class: LeafClass
    gate_class: GateLeafClass
    gate_count: int
    jordan_surgery_eligible: bool
    polygonal_limit_jordan: bool
    messages: list[str]


def classify_leaf_topology(
    leaf: EssentialLeaf,
    *,
    gate_count: int = 2,
    pinch_ratio: float = 0.05,
) -> LeafTopologyAudit:
    """Classify limit leaf topology and gate count."""
    width = _inradius_proxy(leaf)
    leaf_class: LeafClass = "JORDAN_LEAF"
    if width / max(leaf.diameter, 1e-6) < pinch_ratio:
        leaf_class = "PINCHED_LEAF"
    elif len(leaf.closure) > 4:
        leaf_class = "MULTIBOUNDARY_LEAF"
    elif leaf.child_ids and len(leaf.child_ids) > 3:
        leaf_class = "DENDRITIC_LEAF"
    gate_class: GateLeafClass = "NO_CANONICAL_GATE"
    if gate_count == 2:
        gate_class = "TWO_GATE_LEAF"
    elif 2 < gate_count < 20:
        gate_class = "FINITE_MULTIGATE_LEAF"
    elif gate_count >= 20:
        gate_class = "INFINITE_GATE_ACCUMULATION"
    jordan = leaf_class == "JORDAN_LEAF"
    polygonal_jordan = jordan and leaf.level >= 1
    return LeafTopologyAudit(
        leaf_class=leaf_class,
        gate_class=gate_class,
        gate_count=gate_count,
        jordan_surgery_eligible=jordan and gate_class == "TWO_GATE_LEAF",
        polygonal_limit_jordan=polygonal_jordan,
        messages=[f"Leaf {leaf.leaf_id}: {leaf_class}, gates={gate_count}"],
    )


def _inradius_proxy(leaf: EssentialLeaf) -> float:
    if leaf.area <= 0:
        return 0.0
    return (leaf.area / 3.14159) ** 0.5
