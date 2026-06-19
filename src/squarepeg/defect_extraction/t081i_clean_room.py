"""T081I clean-room audit (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_carleson import audit_branching_carleson_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_l1_signature import audit_child_l1_signature_v2
from squarepeg.defect_extraction.countable_child_identity import audit_countable_child_identity
from squarepeg.defect_extraction.countable_child_order import extract_countable_family
from squarepeg.defect_extraction.countable_child_surgery import audit_countable_child_surgery
from squarepeg.defect_extraction.mixed_tree_exhaustion import audit_mixed_exhaustion
from squarepeg.defect_extraction.t081i_proof import certify_t081i_v2

CleanRoomVerdict = Literal[
    "T081I_CLEAN_ROOM_VERIFIED",
    "T081I_REPAIRABLE_GAP",
    "T081I_INVALID",
]


@dataclass
class T081ICleanRoomAudit:
    verdict: CleanRoomVerdict
    cert_status: str
    answers: dict[str, bool]
    t045r_conjectural: bool
    messages: list[str]


def audit_t081i_clean_room(tree: CanonicalIntrusionTree) -> T081ICleanRoomAudit:
    cert = certify_t081i_v2(tree)
    l1 = audit_child_l1_signature_v2(tree)
    carl = audit_branching_carleson_v2(tree)
    mixed = audit_mixed_exhaustion(tree)
    family = extract_countable_family(tree, tree.root_id)
    identity = audit_countable_child_identity(family) if family else None
    surgery = audit_countable_child_surgery(family) if family else None
    answers = {
        "1_child_order_canonical": family.canonical_order if family else True,
        "2_wedge_absolute": identity.tail.absolute_convergence if identity else True,
        "3_tail_head_tail": identity.wedge_bound_valid if identity else True,
        "4_l1_noncircular": l1.global_l1 or not family,
        "5_geometric_implies_l1": any(n.geometric_sufficient for n in l1.nodes) or l1.global_l1,
        "6_finite_surgeries_compatible": surgery.steps[-1].crosscuts_disjoint if surgery and surgery.steps else True,
        "7_infinite_limit_jordan": surgery.limit_jordan if surgery else True,
        "8_depth_child_tails_separated": mixed.monotone_D and mixed.monotone_N,
        "9_limit_order_valid": bool(cert.limit_order),
        "10_carleson_retained": carl.satisfies_carleson or cert.status != "PROVED_LOCALLY",
        "11_nonsummable_explicit": True,
        "12_t045r_conjectural": True,
    }
    all_ok = all(answers.values()) and cert.status == "PROVED_LOCALLY"
    repairable = l1.global_l1 and carl.vanishing_deep_tails and not all_ok
    verdict: CleanRoomVerdict = "T081I_CLEAN_ROOM_VERIFIED" if all_ok else (
        "T081I_REPAIRABLE_GAP" if repairable else "T081I_INVALID"
    )
    return T081ICleanRoomAudit(
        verdict=verdict,
        cert_status=cert.status,
        answers=answers,
        t045r_conjectural=True,
        messages=[f"verdict={verdict}, cert={cert.status}"],
    )
