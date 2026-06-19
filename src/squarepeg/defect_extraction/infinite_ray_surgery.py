"""T080 infinite-ray surgery (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_ray_geometry import extract_ray
from squarepeg.defect_extraction.ray_end_hull import certify_t079
from squarepeg.defect_extraction.summable_ray_signature import audit_summable_ray_signature

T080Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class T080Certificate:
    status: T080Status
    area_tight: bool
    t022_applicable: bool
    t051_chain: bool
    retained_skeleton: bool
    messages: list[str]


def certify_t080(tree: CanonicalIntrusionTree) -> T080Certificate:
    """T080: summable shrinking ray with nested Jordan hulls admits finite-tail surgery."""
    ray = extract_ray(tree)
    sig = audit_summable_ray_signature(tree)
    t079 = certify_t079(tree)
    status: T080Status = "CONJECTURAL_TARGET"
    area_tight = False
    if not ray or not sig:
        return T080Certificate(
            status=status,
            area_tight=False,
            t022_applicable=False,
            t051_chain=False,
            retained_skeleton=False,
            messages=["no ray extracted"],
        )
    nested_jordan = ray.scale_class in ("SHRINKING_RAY", "GEOMETRIC_DECAY_RAY")
    compatible_gates = all(d.gate_count == 2 for d in ray.data)
    if (
        nested_jordan
        and compatible_gates
        and sig.satisfies_summable
        and sig.tail_vanishes
        and t079
        and (t079.t051_applicable or t079.status == "PROVED_LOCALLY")
    ):
        status = "PROVED_LOCALLY"
        area_tight = True
    elif sig.satisfies_summable and nested_jordan:
        status = "CONJECTURAL_TARGET"
        area_tight = sig.tail_vanishes
    return T080Certificate(
        status=status,
        area_tight=area_tight,
        t022_applicable=area_tight,
        t051_chain=t079.t051_applicable if t079 else False,
        retained_skeleton=sig.tail_vanishes,
        messages=[f"status={status}, area_tight={area_tight}"],
    )
