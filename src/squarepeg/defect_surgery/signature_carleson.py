"""SIGNATURE_CARLESON and T043R (Directive 024)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_surgery.attachment_chain import ChainControls, attachment_chain_area, v_att2_squared
from squarepeg.defect_surgery.packet_disk import PacketDisk

T043RStatus = Literal["PROVED_LOCALLY", "CONJECTURAL_TARGET", "PRECISE_GAP"]

SignatureVersion = Literal["A_linear_mass", "B_att2_variation", "C_fat_packing", "D_bounded_multiplicity"]


@dataclass
class SignatureCarlesonAudit:
    max_diameter_vanishes: bool
    intervals_disjoint: bool
    chord_safe: bool
    beta_skeleton_vanishes: bool
    attachment_area_vanishes: bool
    endpoint_corrections_vanish: bool
    satisfies_signature: bool
    messages: list[str] = field(default_factory=list)


@dataclass
class RetainedSkeletonModulus:
    """beta_n(delta): max retained-component area sum on |J|<=delta."""

    delta: float
    beta: float


def audit_signature_carleson(
    *,
    max_diam: float,
    disjoint: bool,
    chord_safe: bool,
    beta: float,
    a_att_sup: float,
    endpoint_corr: float = 0.0,
) -> SignatureCarlesonAudit:
    ok_d = max_diam < 0.02
    ok_b = beta < 0.01
    ok_a = a_att_sup < 0.01
    ok_e = endpoint_corr < 0.01
    sat = ok_d and disjoint and chord_safe and ok_b and ok_a and ok_e
    return SignatureCarlesonAudit(
        max_diameter_vanishes=ok_d,
        intervals_disjoint=disjoint,
        chord_safe=chord_safe,
        beta_skeleton_vanishes=ok_b,
        attachment_area_vanishes=ok_a,
        endpoint_corrections_vanish=ok_e,
        satisfies_signature=sat,
        messages=[
            "SIGNATURE_CARLESON: explicit attachment-chain control required",
            "Square mass mu_2 alone is INSUFFICIENT (Directive 024 counterexample)",
        ],
    )


def version_implies_signature(version: SignatureVersion) -> bool | None:
    """Known implications toward SIGNATURE_CARLESON."""
    if version == "B_att2_variation":
        return None  # true sup (2)-var needs extra structure (Directive 025)
    if version == "A_linear_mass":
        return None
    if version == "C_fat_packing":
        return None
    if version == "D_bounded_multiplicity":
        return None
    return None


def t043r_statement() -> str:
    return (
        "T043R (CONJECTURAL_TARGET): P_n -> gamma uniformly, maximal chord-safe forests "
        "with SIGNATURE_CARLESON => Q_n area-tight => T022 rectangular pegs."
    )
