"""Infinite-center order connection (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.multicenter_thick_leaf import audit_multicenter_thick, center_chart_count
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.nonsummable_concentration import certify_t076
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet


@dataclass
class InfiniteCenterOrderAudit:
    center_count: int
    order_width_diverges: bool
    infinite_width_infinite_center: bool
    reconciled_label: str
    messages: list[str]


def audit_infinite_center_order(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    eta: float = 0.15,
    K: int = 4,
) -> InfiniteCenterOrderAudit:
    """Connect diffuse order residual to INFINITE_WIDTH_INFINITE_CENTER_LAMINATION."""
    mc = audit_multicenter_thick(leaf, eta=eta, K=K)
    t076 = certify_t076(gate_set, K=K)
    width_div = t076.intrinsic_nonsummable and t076.branch == "DIFFUSE_ORDER_INTERACTION"
    iwic = (
        mc.center_count > K
        and width_div
        and mc.center_class in ("INFINITE_CENTER_THICK", "MULTICENTER_THICK_WINDING_LAMINATION")
    )
    label = "INFINITE_WIDTH_INFINITE_CENTER_LAMINATION" if iwic else mc.center_class
    return InfiniteCenterOrderAudit(
        center_count=mc.center_count,
        order_width_diverges=width_div,
        infinite_width_infinite_center=iwic,
        reconciled_label=label,
        messages=[f"centers={mc.center_count}, iwic={iwic}"],
    )
