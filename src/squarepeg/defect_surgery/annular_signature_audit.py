"""Annular forest attachment geometry classification (Directive 025)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.annular_surgery_class import audit_annular_isolated
from squarepeg.defect_surgery.t043r_proof import T043RProofCertificate, certify_t043r
from squarepeg.defect_surgery.nested_forest import PacketForest

AnnularAttachmentClass = Literal[
    "simple_attachment_chain",
    "monotone_angular_chain",
    "bounded_winding",
    "bounded_local_multiplicity",
    "none_of_above",
]

T044RStatus = Literal["PROVED_LOCALLY", "CONTROLLED_FULL_BRIDGE_TARGET", "PRECISE_GAP"]


@dataclass
class AnnularSignatureClassification:
    annular_isolated: bool
    two_gate: bool
    attachment_class: AnnularAttachmentClass
    implies_simple_signature: bool
    implies_bounded_winding: bool
    implies_bounded_multiplicity: bool
    t044r_status: T044RStatus
    message: str


def classify_annular_attachment() -> AnnularSignatureClassification:
    """
    Two-gate annular geometry implies bounded local multiplicity (few gates per short J)
    but NOT automatic simple chain or monotone angle without extra hypotheses.

    Annular => SIGNATURE_CARLESON remains open (Outcome B/C).
    """
    ann = audit_annular_isolated()
    return AnnularSignatureClassification(
        annular_isolated=ann.in_D_ann_surg,
        two_gate=ann.two_gate,
        attachment_class="bounded_local_multiplicity",
        implies_simple_signature=False,
        implies_bounded_winding=False,
        implies_bounded_multiplicity=True,
        t044r_status="CONTROLLED_FULL_BRIDGE_TARGET",
        message=(
            "Annular two-gate geometry gives bounded multiplicity on short J; "
            "full SIGNATURE_CARLESON requires proved beta/sigma vanishing — open."
        ),
    )


def t044r_statement() -> str:
    return (
        "T044R (CONTROLLED_FULL_BRIDGE_TARGET): ANNULAR_SURGERY_FOREST with proved "
        "sufficient signature class => positive scale square + shrinking T043R => peg."
    )


def audit_t044r_with_t043r(forest: PacketForest) -> tuple[AnnularSignatureClassification, T043RProofCertificate]:
    cls = classify_annular_attachment()
    cert = certify_t043r(forest=forest, beta=0.005, sigma=0.005)
    return cls, cert
