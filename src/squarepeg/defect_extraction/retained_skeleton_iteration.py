"""Retained skeleton iteration (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.retained_skeleton_control import beta_on_interval
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import Point

CoverStatus = Literal["COVER_COMPLETE", "RESIDUAL_BAD_INTERVAL"]


@dataclass
class RetainedIteration:
    level: int
    beta: float
    status: CoverStatus


def iterate_retained_skeleton(
    vertices: list[Point],
    forest: PacketForest,
    i0: int,
    i1: int,
    *,
    max_levels: int = 3,
    threshold: float = 0.01,
) -> list[RetainedIteration]:
    results: list[RetainedIteration] = []
    for lv in range(max_levels):
        beta = beta_on_interval(vertices, forest, i0, i1)
        st: CoverStatus = "COVER_COMPLETE" if beta < threshold else "RESIDUAL_BAD_INTERVAL"
        results.append(RetainedIteration(level=lv, beta=beta, status=st))
        if st == "COVER_COMPLETE":
            break
    return results
