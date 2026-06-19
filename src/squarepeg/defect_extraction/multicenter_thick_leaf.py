"""Multicenter thick leaves and infinite-center residual (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.thin_leaf_geometry import leaf_width

ThickClass = Literal[
    "FINITE_CENTER_THICK",
    "INFINITE_CENTER_THICK",
    "MULTICENTER_THICK_WINDING_LAMINATION",
]


@dataclass
class CenterChartAudit:
    leaf_id: str
    center_count: int
    eta: float
    thick: bool
    center_class: ThickClass


def center_chart_count(leaf: EssentialLeaf, *, eta: float = 0.15) -> int:
    """N_c(L, eta): minimum star-shaped charts at scale eta diam L."""
    w = leaf_width(leaf)
    if w >= eta * leaf.diameter:
        return 1
    if leaf.child_ids and len(leaf.child_ids) > 1:
        return len(leaf.child_ids) + 1
    if leaf.diameter > 1.5:
        return 3
    return 1


def audit_multicenter_thick(leaf: EssentialLeaf, *, eta: float = 0.15, K: int = 4) -> CenterChartAudit:
    nc = center_chart_count(leaf, eta=eta)
    w = leaf_width(leaf)
    thick = w >= 0.12 * leaf.diameter
    center_class: ThickClass = "FINITE_CENTER_THICK"
    if nc > K:
        center_class = "INFINITE_CENTER_THICK" if eta < 0.2 else "MULTICENTER_THICK_WINDING_LAMINATION"
    return CenterChartAudit(
        leaf_id=leaf.leaf_id,
        center_count=nc,
        eta=eta,
        thick=thick,
        center_class=center_class,
    )
