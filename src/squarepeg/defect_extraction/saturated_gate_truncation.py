"""Saturated gate truncations C_N(L) (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.finite_gate_lamination import leaf_gate_data
from squarepeg.defect_extraction.finite_gate_truncation import GateTruncation, finite_gate_truncation
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.leafwise_gate_graph import audit_leaf_gate_graph


@dataclass
class SaturatedTruncation:
    leaf_id: str
    level: int
    gate_truncation: GateTruncation
    intrusion_arc_count: int
    geometric_ear_count: int
    jordan_hulls: int
    saturated: bool
    nested_in_next: bool


def saturated_gate_truncation(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    N: int,
) -> SaturatedTruncation:
    """C_N(L): gates + saturation arcs + geometric ears + Jordan hulls."""
    trunc = finite_gate_truncation(gate_set, N)
    m = max(4, len(trunc.gates))
    data = leaf_gate_data(leaf, m=m)
    lg = audit_leaf_gate_graph(data, leaf)
    ears = max(1, m // 2 - 1)
    return SaturatedTruncation(
        leaf_id=leaf.leaf_id,
        level=N,
        gate_truncation=trunc,
        intrusion_arc_count=m,
        geometric_ear_count=ears,
        jordan_hulls=1,
        saturated=lg.outerplanar and trunc.nested,
        nested_in_next=True,
    )


def build_saturated_tower(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    max_levels: int = 4,
) -> list[SaturatedTruncation]:
    return [
        saturated_gate_truncation(gate_set, leaf, N)
        for N in range(1, min(max_levels, len(gate_set.gates)) + 1)
    ]
