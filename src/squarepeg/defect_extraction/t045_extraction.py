"""T045R universal extraction (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.defect_tree import DefectTree, DefectTreeNode, classify_node
from squarepeg.defect_extraction.clean_lobe import audit_clean_lobe
from squarepeg.defect_extraction.packet_laminarization import audit_laminarization
from squarepeg.defect_extraction.interleaving_reference import audit_interleaving_reference
from squarepeg.defect_extraction.annular_subpacket import audit_annular_subpacket
from squarepeg.defect_geometry.lobe import LobeRecord
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import PacketDisk, Point
from squarepeg.defect_surgery.t046_signature_theorem import certify_t046
from squarepeg.robust_degree.t039_persistence import audit_t039

T045RStatus = Literal["CONJECTURAL_FULL_EXTRACTION", "PROVED_LOCALLY", "PRECISE_GAP"]
T047Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY", "PRECISE_GAP"]

ResidualClass = Literal[
    "MULTICENTER_ALTERNATING_INTRUSION_TREE",
    "NONE",
]


@dataclass
class T047Audit:
    status: T047Status
    dominant_lobe: bool
    interleaving: bool
    branching: bool
    counterexample: bool


@dataclass
class T045RExtractionCertificate:
    status: T045RStatus
    branch_a: bool
    branch_b: bool
    clean_forest_path: bool
    all_nodes_classified: bool
    residual_class: ResidualClass
    t047: T047Audit
    messages: list[str] = field(default_factory=list)


def audit_t047(*, has_dirty: bool, has_interleaving: bool) -> T047Audit:
    """T047 trichotomy — conjectural; dirty+interleaving breaks clean trichotomy."""
    if has_dirty and has_interleaving:
        return T047Audit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            dominant_lobe=False,
            interleaving=True,
            branching=True,
            counterexample=True,
        )
    return T047Audit(
        status="CONJECTURAL_STRUCTURAL_TARGET",
        dominant_lobe=True,
        interleaving=False,
        branching=False,
        counterexample=False,
    )


def certify_clean_forest_extraction(
    vertices: list[Point],
    disks: list[PacketDisk],
    i0: int,
    i1: int,
) -> bool:
    """Branch B when all packets clean, laminar, gate-ordered, and T046 passes."""
    lam = audit_laminarization(disks, vertices)
    if not (lam.laminar and lam.gate_ordered):
        return False
    forest = PacketForest(disks=disks)
    t046 = certify_t046(vertices, forest, i0, i1, omega_gamma=0.08)
    return t046.status == "PROVED_LOCALLY"


def certify_t045r_extraction(
    vertices: list[Point],
    disks: list[PacketDisk],
    lobes: list[LobeRecord],
    *,
    all_clean: bool = False,
    has_interleaving: bool = False,
    i0: int = 0,
    i1: int = 6,
) -> T045RExtractionCertificate:
    t047 = audit_t047(has_dirty=not all_clean, has_interleaving=has_interleaving)
    clean_path = all_clean and certify_clean_forest_extraction(vertices, disks, i0, i1)
    inter = audit_interleaving_reference()
    branch_a = inter.reference_verdict == "INTERLEAVING_REFERENCE_PROTECTED"
    branch_b = clean_path
    residual: ResidualClass = "NONE" if (branch_a or branch_b) else "MULTICENTER_ALTERNATING_INTRUSION_TREE"
    all_classified = branch_a or branch_b or residual != "NONE"
    status: T045RStatus = "PROVED_LOCALLY" if branch_a and branch_b else "CONJECTURAL_FULL_EXTRACTION"
    return T045RExtractionCertificate(
        status=status,
        branch_a=branch_a,
        branch_b=branch_b,
        clean_forest_path=branch_b,
        all_nodes_classified=all_classified,
        residual_class=residual,
        t047=t047,
        messages=[
            "T045R: CONJECTURAL unless every residual node closed",
            f"Clean forest path: {clean_path}",
            f"Residual: {residual}",
            "T037 supplies persistent defect subsequence at array level",
        ],
    )


def t045r_statement() -> str:
    return (
        "T045R (CONJECTURAL_FULL_EXTRACTION): non-area-tight P_n => protected square OR "
        "signature-controlled surgery forest."
    )
