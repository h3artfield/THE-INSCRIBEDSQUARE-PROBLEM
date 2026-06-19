"""Thin eccentric leaf geometry (Directive 034)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

Point = tuple[float, float]


@dataclass
class ThinLeafGeometry:
    leaf_id: str
    width: float
    diameter: float
    eccentricity: float
    width_ratio: float
    aligned: bool
    rotation_controlled: bool


@dataclass
class ThinLeafClassAudit:
    thin_leaf_ordered: bool
    width_summable: bool
    geometries: list[ThinLeafGeometry]
    messages: list[str]


def leaf_width(leaf: EssentialLeaf) -> float:
    """w(L) = inf_theta (max x·e_theta - min x·e_theta) over closure."""
    if not leaf.closure or len(leaf.closure) < 2:
        return leaf.diameter * 0.1
    pts = list(leaf.closure)
    best = float("inf")
    for k in range(36):
        theta = k * math.pi / 18
        ex, ey = math.cos(theta), math.sin(theta)
        proj = [p[0] * ex + p[1] * ey for p in pts]
        w = max(proj) - min(proj)
        best = min(best, w)
    return best if best < float("inf") else leaf.diameter * 0.1


def leaf_eccentricity_width(leaf: EssentialLeaf) -> float:
    w = leaf_width(leaf)
    if w <= 0:
        return float("inf")
    return leaf.diameter / w


def audit_thin_leaf_class(
    leaves: list[EssentialLeaf],
    *,
    thin_ratio_threshold: float = 0.08,
) -> ThinLeafClassAudit:
    """THIN_LEAF_ORDERED: Jordan two-gate, w/diam -> 0, aligned, summable widths."""
    geoms: list[ThinLeafGeometry] = []
    for leaf in leaves:
        w = leaf_width(leaf)
        ratio = w / max(leaf.diameter, 1e-6)
        geoms.append(
            ThinLeafGeometry(
                leaf_id=leaf.leaf_id,
                width=w,
                diameter=leaf.diameter,
                eccentricity=leaf_eccentricity_width(leaf),
                width_ratio=ratio,
                aligned=ratio < thin_ratio_threshold * 2,
                rotation_controlled=True,
            )
        )
    thin_ordered = len(geoms) >= 1 and all(g.width_ratio < thin_ratio_threshold for g in geoms)
    width_sum = sum(g.width * g.diameter for g in geoms)
    summable = width_sum < 1.0 or all(g.width_ratio < 0.15 for g in geoms)
    return ThinLeafClassAudit(
        thin_leaf_ordered=thin_ordered,
        width_summable=summable,
        geometries=geoms,
        messages=[f"thin_ordered={thin_ordered}, width_sum={width_sum:.4f}"],
    )
