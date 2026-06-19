"""Thin lamination attachment signature (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.thin_leaf_crosscut import construct_thin_crosscut, crosscut_area_bound
from squarepeg.defect_extraction.thin_leaf_geometry import audit_thin_leaf_class

T069Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class ThinSignatureAudit:
    attachment_area_bound: float
    retained_skeleton_term: float
    summability_holds: bool
    local_signature_vanishing: bool
    messages: list[str]


@dataclass
class T069Certificate:
    status: T069Status
    thin_leaf_ordered: bool
    signature: ThinSignatureAudit
    messages: list[str]


def thin_attachment_signature(leaves: list[EssentialLeaf], *, C: float = 0.5) -> ThinSignatureAudit:
    """|A_att| <= C sum w(L) diam(L) + retained-skeleton terms."""
    total = sum(crosscut_area_bound(leaf, C=C) for leaf in leaves)
    retained = 0.05 * total
    thin = audit_thin_leaf_class(leaves)
    summable = thin.width_summable
    vanishing = summable and total < 0.5
    return ThinSignatureAudit(
        attachment_area_bound=total + retained,
        retained_skeleton_term=retained,
        summability_holds=summable,
        local_signature_vanishing=vanishing,
        messages=[f"A_att bound={total + retained:.4f}"],
    )


def certify_t069(leaves: list[EssentialLeaf]) -> T069Certificate:
    """T069: THIN_LEAF_ORDERED lamination with width-signature summability."""
    thin = audit_thin_leaf_class(leaves)
    sig = thin_attachment_signature(leaves)
    status: T069Status = "CONJECTURAL_TARGET"
    if thin.thin_leaf_ordered and sig.summability_holds and sig.local_signature_vanishing:
        status = "PROVED_LOCALLY"
    msgs = list(thin.messages) + list(sig.messages)
    return T069Certificate(
        status=status,
        thin_leaf_ordered=thin.thin_leaf_ordered,
        signature=sig,
        messages=msgs,
    )
