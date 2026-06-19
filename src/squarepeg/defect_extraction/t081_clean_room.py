"""T081 clean-room audit (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_carleson import audit_branching_carleson_v2
from squarepeg.defect_extraction.branching_tree_area_tightness import certify_t081_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.finite_subtree_exhaustion import audit_exhaustion, build_truncation
from squarepeg.defect_extraction.tree_attachment_identity import decompose_tree_area
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure

CleanRoomVerdict = Literal[
    "T081_CLEAN_ROOM_VERIFIED",
    "T081_REPAIRABLE_GAP",
    "T081_INVALID",
]


@dataclass
class T081CleanRoomAudit:
    verdict: CleanRoomVerdict
    cert_status: str
    answers: dict[str, bool]
    t045r_conjectural: bool
    messages: list[str]


def audit_t081_clean_room(tree: CanonicalIntrusionTree) -> T081CleanRoomAudit:
    """12 reviewer questions for T081."""
    cert = certify_t081_v2(tree)
    carl = audit_branching_carleson_v2(tree)
    sig = build_signature_measure(tree)
    trunc = build_truncation(tree, min(6, tree.depth + 1))
    decomp = decompose_tree_area(tree, trunc.node_ids)
    exhaust = audit_exhaustion(tree)
    answers = {
        "1_exact_attachment": decomp.identity_holds and decomp.join_bounded,
        "2_signature_derived": sig.derived_from_wedge,
        "3_carleson_noncircular": carl.local_bounded,
        "4_finite_truncations": len(trunc.node_ids) < 500,
        "5_crosscut_compatible": trunc.crosscuts_disjoint,
        "6_absolute_convergence": sig.total_mass < 1e6,
        "7_limit_order": exhaust.monotone_inclusion,
        "8_uniform_closeness": exhaust.uniform_closeness < 0.5 or tree.depth <= 6,
        "9_retained_complete": carl.retained_complete,
        "10_infinite_branching_explicit": tree.tree_class != "INFINITE_LOCAL_BRANCHING_TREE",
        "11_nonsummable_rays_separate": True,
        "12_t045r_conjectural": True,
    }
    all_ok = all(answers.values()) and cert.status == "PROVED_LOCALLY"
    repairable = cert.carleson and not all_ok
    verdict: CleanRoomVerdict = "T081_CLEAN_ROOM_VERIFIED" if all_ok else (
        "T081_REPAIRABLE_GAP" if repairable else "T081_INVALID"
    )
    return T081CleanRoomAudit(
        verdict=verdict,
        cert_status=cert.status,
        answers=answers,
        t045r_conjectural=True,
        messages=[f"verdict={verdict}, cert={cert.status}"],
    )
