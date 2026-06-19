"""T081I proof — countably branching tree surgery (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_carleson import audit_branching_carleson_v2
from squarepeg.defect_extraction.branching_tree_area_tightness import certify_t081_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_l1_signature import audit_child_l1_signature_v2
from squarepeg.defect_extraction.countable_child_order import extract_countable_family
from squarepeg.defect_extraction.countable_child_surgery import audit_countable_child_surgery
from squarepeg.defect_extraction.mixed_tree_exhaustion import audit_mixed_exhaustion

T081IStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class T081IProofCertificate:
    status: T081IStatus
    area_tight: bool
    t022_applicable: bool
    child_l1: bool
    carleson: bool
    mixed_exhaustion: bool
    limit_order: str
    messages: list[str]


def certify_t081i_v2(tree: CanonicalIntrusionTree) -> T081IProofCertificate:
    """T081I: CHILD_L1_SIGNATURE + Carleson -> area-tight two-parameter exhaustion."""
    l1 = audit_child_l1_signature_v2(tree)
    carl = audit_branching_carleson_v2(tree)
    mixed = audit_mixed_exhaustion(tree)
    t081 = certify_t081_v2(tree)
    child_ok = True
    for nid, node in tree.nodes.items():
        if len(node.child_ids) >= 8:
            fam = extract_countable_family(tree, nid)
            if fam:
                surg = audit_countable_child_surgery(fam)
                child_ok = child_ok and surg.limit_jordan
    status: T081IStatus = "CONJECTURAL_TARGET"
    area_tight = False
    has_countable = any(len(n.child_ids) >= 8 for n in tree.nodes.values())
    if (
        l1.global_l1
        and l1.uniform_local
        and carl.satisfies_carleson
        and mixed.signature_represented
        and mixed.truncations[-1].jordan if mixed.truncations else False
        and child_ok
    ):
        status = "PROVED_LOCALLY"
        area_tight = True
    elif l1.global_l1 and t081.status == "PROVED_LOCALLY" and not has_countable:
        area_tight = t081.area_tight
    return T081IProofCertificate(
        status=status,
        area_tight=area_tight,
        t022_applicable=area_tight and status == "PROVED_LOCALLY",
        child_l1=l1.global_l1,
        carleson=carl.satisfies_carleson,
        mixed_exhaustion=mixed.signature_represented,
        limit_order="n, delta, N(D,delta), D",
        messages=[f"status={status}, l1={l1.global_l1}, carleson={carl.satisfies_carleson}"],
    )
