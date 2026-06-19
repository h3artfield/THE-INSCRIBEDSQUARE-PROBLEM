"""Intrusion tree end space and end measures (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_ray_geometry import extract_ray
from squarepeg.defect_extraction.summable_ray_signature import audit_summable_ray_signature

EndMeasureClass = Literal[
    "ATOMIC",
    "COUNTABLY_ATOMIC",
    "DIFFUSE_CANTOR",
    "FINITE_CENTERS",
    "INFINITE_CENTERS",
]


@dataclass
class TreeEnd:
    end_id: str
    spatial_point: tuple[float, float] | None
    param_limit: float
    sign: int
    accumulated_signature: float
    center_path: list[tuple[float, float]]
    gate_order_type: str


@dataclass
class EndMeasure:
    ends: list[TreeEnd]
    measure_class: EndMeasureClass
    total_mass: float
    truncation_independent: bool


@dataclass
class EndDecompositionAudit:
    end_measure: EndMeasure
    atomic_summable: bool
    routes_to_t080: bool
    diffuse_residual: bool
    messages: list[str]


def build_end_space(tree: CanonicalIntrusionTree) -> list[TreeEnd]:
    """Assign data to tree ends (leaf nodes as proxy)."""
    ends: list[TreeEnd] = []
    for nid, node in tree.nodes.items():
        if node.child_ids:
            continue
        ends.append(
            TreeEnd(
                end_id=nid,
                spatial_point=node.center,
                param_limit=node.param_interval[1],
                sign=node.sign,
                accumulated_signature=node.defect,
                center_path=[node.center],
                gate_order_type=node.gate_class,
            )
        )
    return ends


def build_end_measure(tree: CanonicalIntrusionTree) -> EndMeasure:
    ends = build_end_space(tree)
    total = sum(e.accumulated_signature for e in ends)
    centers = len({(round(e.spatial_point[0], 1), round(e.spatial_point[1], 1)) for e in ends if e.spatial_point})
    if len(ends) == 1:
        mc: EndMeasureClass = "ATOMIC"
    elif len(ends) <= 8:
        mc = "COUNTABLY_ATOMIC" if centers <= 4 else "FINITE_CENTERS"
    elif centers > 8:
        mc = "INFINITE_CENTERS"
    else:
        mc = "DIFFUSE_CANTOR"
    return EndMeasure(
        ends=ends,
        measure_class=mc,
        total_mass=total,
        truncation_independent=True,
    )


def audit_end_decomposition(tree: CanonicalIntrusionTree) -> EndDecompositionAudit:
    em = build_end_measure(tree)
    sig = audit_summable_ray_signature(tree)
    atomic_summable = em.measure_class == "ATOMIC" and sig is not None and sig.satisfies_summable
    routes_t080 = atomic_summable
    diffuse = em.measure_class in ("DIFFUSE_CANTOR", "INFINITE_CENTERS")
    return EndDecompositionAudit(
        end_measure=em,
        atomic_summable=atomic_summable,
        routes_to_t080=routes_t080,
        diffuse_residual=diffuse,
        messages=[f"class={em.measure_class}, atomic_summable={atomic_summable}"],
    )
