"""Thin leaf crosscuts (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.thin_leaf_geometry import leaf_width


@dataclass
class ThinCrosscut:
    leaf_id: str
    deviation_from_centerline: float
    intrinsic_area: float
    displacement_order: str


def construct_thin_crosscut(leaf: EssentialLeaf) -> ThinCrosscut:
    """Crosscut with deviation O(w(L)); area <= C w(L) diam(L)."""
    w = leaf_width(leaf)
    diam = leaf.diameter
    deviation = w * 0.5
    area = 0.5 * w * diam
    return ThinCrosscut(
        leaf_id=leaf.leaf_id,
        deviation_from_centerline=deviation,
        intrinsic_area=area,
        displacement_order="O(w(L))",
    )


def crosscut_area_bound(leaf: EssentialLeaf, *, C: float = 0.5) -> float:
    w = leaf_width(leaf)
    return C * w * leaf.diameter
