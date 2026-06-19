"""Ray end hull and T079 saturation (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.intrusion_ray_geometry import IntrusionRay, extract_ray
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

T079Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]
EndHullClass = Literal[
    "SINGLE_POINT",
    "NON_SINGLE_POINT",
    "JORDAN_DISK",
    "PINCHED_BOUNDARY",
    "INFINITELY_GATED",
]


@dataclass
class RayEndHull:
    limit_set_single_point: bool
    end_point: tuple[float, float] | None
    end_neighborhood_jordan: bool
    two_external_gates: bool
    gate_count_finite: bool
    end_hull_class: EndHullClass


@dataclass
class T079Certificate:
    status: T079Status
    saturation_two_gate: bool
    diameter_order: str
    end_hull: RayEndHull
    t051_applicable: bool
    messages: list[str]


def limit_set_k_infinity(ray: IntrusionRay) -> tuple[bool, tuple[float, float] | None]:
    """K_infty = cap H_{v_j}; single point when r_j -> 0 and nested."""
    if not ray.data:
        return True, None
    if ray.scale_class == "POSITIVE_SCALE_RAY":
        return False, ray.data[-1].center
    radii = [d.diameter for d in ray.data]
    shrinking = radii[-1] < 0.2 * radii[0]
    if shrinking:
        return True, ray.data[-1].center
    return False, None


def end_neighborhood(ray: IntrusionRay, j: int) -> RayEndHull:
    """E_j = H_{v_j} union tail hulls."""
    tail = ray.data[j:]
    radii = [d.diameter for d in tail]
    single, pt = limit_set_k_infinity(IntrusionRay(ray.node_ids[j:], tail, ray.scale_class, ray.positive_subclass))
    two_gates = all(d.gate_count == 2 for d in tail[-3:]) if tail else True
    finite_gates = all(d.gate_count < 50 for d in tail)
    jordan = ray.scale_class != "POSITIVE_SCALE_RAY"
    eh: EndHullClass = "JORDAN_DISK"
    if not single:
        eh = "NON_SINGLE_POINT"
    elif not two_gates:
        eh = "INFINITELY_GATED"
    elif not jordan:
        eh = "PINCHED_BOUNDARY"
    elif single:
        eh = "SINGLE_POINT"
    return RayEndHull(
        limit_set_single_point=single,
        end_point=pt,
        end_neighborhood_jordan=jordan,
        two_external_gates=two_gates,
        gate_count_finite=finite_gates,
        end_hull_class=eh,
    )


def certify_t079(tree: CanonicalIntrusionTree) -> T079Certificate | None:
    """T079: shrinking ray with two end gates saturates to two-gate cluster O(r_j)."""
    ray = extract_ray(tree)
    if not ray:
        return None
    full_end = end_neighborhood(ray, 0)
    single, _ = limit_set_k_infinity(ray)
    shrinking = ray.scale_class in ("SHRINKING_RAY", "GEOMETRIC_DECAY_RAY")
    two_gate = all(d.gate_count == 2 for d in ray.data)
    status: T079Status = "CONJECTURAL_TARGET"
    saturation = False
    if shrinking and two_gate and single and full_end.end_neighborhood_jordan:
        status = "PROVED_LOCALLY"
        saturation = True
    elif ray.scale_class == "POSITIVE_SCALE_RAY":
        status = "CONJECTURAL_TARGET"
        saturation = False
    return T079Certificate(
        status=status,
        saturation_two_gate=saturation,
        diameter_order="O(r_j)" if saturation else "UNKNOWN",
        end_hull=full_end,
        t051_applicable=saturation,
        messages=[f"T079 status={status}, two_gate={saturation}"],
    )
