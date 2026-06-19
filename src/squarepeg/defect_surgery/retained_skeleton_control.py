"""Retained-skeleton control for annular surgery (Directive 026)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_surgery.attachment_signature import beta_retained_modulus
from squarepeg.defect_surgery.exact_component_decomposition import decompose_cyclic_interval
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import Point


@dataclass
class RetainedSkeletonAudit:
    beta: float
    max_retained_area: float
    vanishes: bool


def beta_on_interval(
    vertices: list[Point],
    forest: PacketForest,
    i0: int,
    i1: int,
) -> float:
    decomp = decompose_cyclic_interval(vertices, i0, i1, forest)
    return beta_retained_modulus(decomp.components)


def audit_retained_skeleton(
    vertices: list[Point],
    forest: PacketForest,
    i0: int,
    i1: int,
    *,
    threshold: float = 0.01,
) -> RetainedSkeletonAudit:
    decomp = decompose_cyclic_interval(vertices, i0, i1, forest)
    beta = beta_retained_modulus(decomp.components)
    max_a = max((abs(c.intrinsic_area) for c in decomp.components if c.kind == "retained"), default=0.0)
    return RetainedSkeletonAudit(beta=beta, max_retained_area=max_a, vanishes=beta < threshold)
