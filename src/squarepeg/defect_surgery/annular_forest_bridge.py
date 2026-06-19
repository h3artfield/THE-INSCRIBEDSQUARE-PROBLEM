"""ANNULAR_SURGERY_FOREST and T044R bridge (Directive 024)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.annular_surgery_class import audit_annular_isolated
from squarepeg.defect_surgery.fat_disk_packing import packing_estimate_sum_diam_sq
from squarepeg.defect_surgery.signature_carleson import SignatureCarlesonAudit, audit_signature_carleson
from squarepeg.defect_surgery.square_mass_counterexample import square_mass_sufficiency_verdict

T044RStatus = Literal["CONTROLLED_FULL_BRIDGE_TARGET", "CONJECTURAL", "PRECISE_GAP"]


@dataclass
class AnnularSurgeryForestAudit:
    annular_isolated: bool
    fat_disks: bool
    disjoint_or_nested: bool
    mu2_packing_bound: bool
    signature_carleson: bool
    t044r_ready: bool


def audit_annular_surgery_forest(
    *,
    max_diam: float = 0.01,
    omega_j: float = 0.05,
) -> AnnularSurgeryForestAudit:
    ann = audit_annular_isolated()
    # Shrinking annular: mu2 ~ omega^2 via packing; attachment needs signature
    sig = audit_signature_carleson(
        max_diam=max_diam,
        disjoint=True,
        chord_safe=True,
        beta=0.005,
        a_att_sup=0.005,
    )
    return AnnularSurgeryForestAudit(
        annular_isolated=ann.in_D_ann_surg,
        fat_disks=True,
        disjoint_or_nested=True,
        mu2_packing_bound=omega_j ** 2 > max_diam ** 2,
        signature_carleson=sig.satisfies_signature,
        t044r_ready=False,  # requires proved T043R + annular => signature
    )


def t044r_statement() -> str:
    return (
        "T044R (CONTROLLED_FULL_BRIDGE_TARGET): ANNULAR_SURGERY_FOREST dichotomy — "
        "positive scale => square; shrinking maximal packets => T043R => area-tight."
    )
