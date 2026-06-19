"""Annular subpacket extraction T048 (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.packet_shape_audit import ShapeAudit, audit_packet_shape
from squarepeg.defect_geometry.lobe import LobeRecord

T048Status = Literal["CONJECTURAL_GEOMETRIC_TARGET", "PROVED_LOCALLY", "PRECISE_GAP"]


@dataclass
class AnnularSubpacketAudit:
    status: T048Status
    has_annular_subpacket: bool
    has_protected_square: bool
    residual_eccentric: bool


def audit_annular_subpacket(lobe: LobeRecord) -> AnnularSubpacketAudit:
    shape = audit_packet_shape(lobe)
    return AnnularSubpacketAudit(
        status="CONJECTURAL_GEOMETRIC_TARGET",
        has_annular_subpacket=shape.shape_class == "ANNULAR_GRAPH_PACKET",
        has_protected_square=False,
        residual_eccentric=shape.shape_class == "ECCENTRIC_PACKET",
    )


def t048_statement() -> str:
    return "T048 (CONJECTURAL_GEOMETRIC_TARGET): clean same-sign packet => annular subpacket or protected square or residual."
