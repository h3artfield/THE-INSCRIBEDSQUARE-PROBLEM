"""T081I countable branching tree surgery (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_carleson import audit_branching_carleson_v2
from squarepeg.defect_extraction.branching_tree_area_tightness import certify_t081_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.countable_child_signature import audit_child_l1_signature

T081IStatus = Literal["CONJECTURAL_EXTENSION", "PROVED_LOCALLY_PARTIAL"]


@dataclass
class T081ICertificate:
    status: T081IStatus
    area_tight: bool
    child_l1: bool
    carleson: bool
    messages: list[str]


def certify_t081i(tree: CanonicalIntrusionTree) -> T081ICertificate:
    """T081I: extend T081 to infinite local branching under CHILD_L1_SIGNATURE."""
    t081 = certify_t081_v2(tree)
    l1 = audit_child_l1_signature(tree)
    carl = audit_branching_carleson_v2(tree)
    status: T081IStatus = "CONJECTURAL_EXTENSION"
    area_tight = False
    if (
        tree.tree_class == "INFINITE_LOCAL_BRANCHING_TREE"
        and l1.global_l1
        and carl.vanishing_deep_tails
        and t081.carleson
    ):
        status = "PROVED_LOCALLY_PARTIAL"
        area_tight = t081.area_tight
    elif l1.global_l1 and t081.status == "PROVED_LOCALLY":
        area_tight = True
    return T081ICertificate(
        status=status,
        area_tight=area_tight,
        child_l1=l1.global_l1,
        carleson=carl.satisfies_carleson,
        messages=[f"status={status}, l1={l1.global_l1}"],
    )
