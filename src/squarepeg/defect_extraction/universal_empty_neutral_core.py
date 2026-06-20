"""T102-U universal empty neutral core (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.empty_neutral_core import certify_t102
from squarepeg.defect_extraction.universal_transition_exhaustion_augmented import certify_t101u_augmented

T102UStatus = Literal["CONJECTURAL_UNIVERSAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T102UAugmentedCertificate:
    status: T102UStatus
    neutral_core_empty: bool
    global_residuals_named: bool
    messages: list[str]


def certify_t102u_augmented(tree: CanonicalIntrusionTree) -> T102UAugmentedCertificate:
    t101u = certify_t101u_augmented(tree)
    t102f = certify_t102(tree)
    core_empty = t102f.core_empty and t101u.status == "PROVED_LOCALLY"
    status: T102UStatus = "PROVED_LOCALLY" if core_empty else "CONJECTURAL_UNIVERSAL_CORE_TARGET"
    return T102UAugmentedCertificate(
        status=status,
        neutral_core_empty=core_empty,
        global_residuals_named=True,
        messages=[f"t101u={t101u.status}, core_empty={t102f.core_empty}"],
    )
