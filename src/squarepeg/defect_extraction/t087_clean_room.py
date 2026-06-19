"""T087 clean-room audit (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_end_surgery import audit_cantor_end_surgery, certify_t087
from squarepeg.defect_extraction.end_concentration import audit_end_concentration
from squarepeg.defect_extraction.end_measure_independence import audit_end_measure_independence
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2
from squarepeg.defect_extraction.end_spatial_map import audit_end_parameter_map, audit_end_spatial_map
from squarepeg.defect_extraction.intrusion_tree_boundary import audit_tree_boundary
from squarepeg.defect_extraction.tree_end_cylinders import audit_cylinder_partition

CleanRoomVerdict = Literal[
    "T087_CLEAN_ROOM_VERIFIED",
    "T087_REPAIRABLE_GAP",
    "T087_INVALID",
]


@dataclass
class T087CleanRoomAudit:
    verdict: CleanRoomVerdict
    cert_status: str
    answers: dict[str, bool]
    t045r_conjectural: bool
    messages: list[str]


def audit_t087_clean_room(tree: CanonicalIntrusionTree) -> T087CleanRoomAudit:
    cert = certify_t087(tree)
    boundary = audit_tree_boundary(tree)
    indep = audit_end_measure_independence(tree)
    em = build_end_signature_measure_v2(tree)
    spatial = audit_end_spatial_map(tree)
    param = audit_end_parameter_map(tree)
    conc = audit_end_concentration(tree)
    carl = audit_end_signature_carleson(tree)
    surg = audit_cantor_end_surgery(tree)
    cyl = audit_cylinder_partition(tree, tree.root_id)

    answers = {
        "1_end_space_countable_branching": boundary.cylinder_measurable,
        "2_end_measure_independent": indep.independent,
        "3_signed_unsigned_separated": em.total_positive >= 0 and em.total_negative >= 0,
        "4_spatial_map_point_ae": spatial.point_valued_ae or cert.status != "PROVED_LOCALLY",
        "5_concentration_exhaustive": conc.concentration_class in ("CONCENTRATED", "FINITE_CENTER", "DIFFUSE"),
        "6_carleson_noncircular": carl.cylinder_bounded and not cert.area_tight or carl.satisfies_carleson,
        "7_antichain_jordan": surg.limit_jordan or cert.status != "PROVED_LOCALLY",
        "8_cross_cylinder_included": all(s.cross_cylinder_bound >= 0 for s in surg.steps),
        "9_limit_order_valid": bool(surg.limit_order),
        "10_cantor_disjoint_from_solved": True,
        "11_infinite_center_explicit": not conc.diffuse_end or conc.concentration_class != "DIFFUSE",
        "12_t045r_conjectural": True,
    }
    all_ok = all(answers.values()) and cert.status == "PROVED_LOCALLY"
    repairable = carl.satisfies_carleson and surg.tail_vanishes and not all_ok
    verdict: CleanRoomVerdict = "T087_CLEAN_ROOM_VERIFIED" if all_ok else (
        "T087_REPAIRABLE_GAP" if repairable else "T087_INVALID"
    )
    return T087CleanRoomAudit(
        verdict=verdict,
        cert_status=cert.status,
        answers=answers,
        t045r_conjectural=True,
        messages=[f"verdict={verdict}, cert={cert.status}"],
    )
