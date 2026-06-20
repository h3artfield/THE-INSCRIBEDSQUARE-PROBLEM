"""T101-U universal transition exhaustion with augmented datum (Directive 056)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.countable_child_transition_routes import certify_t104
from squarepeg.defect_extraction.gate_measure_weak_closure import certify_t107
from squarepeg.defect_extraction.t105r_measure_closure import certify_t105r
from squarepeg.defect_extraction.t108_exhaustion import certify_t108
from squarepeg.defect_extraction.unbounded_gate_transition_routes import certify_t106
from squarepeg.defect_extraction.universal_transition_exhaustion import certify_t101

T101UStatus = Literal["CONJECTURAL_UNIVERSAL_EXHAUSTION", "PROVED_LOCALLY"]


@dataclass
class T101UAugmentedCertificate:
    status: T101UStatus
    finite_domain: bool
    augmented_infinite: bool
    messages: list[str]


def certify_t101u_augmented(tree: CanonicalIntrusionTree) -> T101UAugmentedCertificate:
    t101f = certify_t101(tree)
    t104 = certify_t104(tree)
    t105r = certify_t105r(tree)
    t106 = certify_t106(tree)
    t107 = certify_t107(tree)
    t108 = certify_t108(tree)
    finite_ok = t101f.status in ("PROVED_FINITE_DOMAIN", "PROVED_LOCALLY")
    infinite_ok = (
        t104.status == "PROVED_LOCALLY"
        and t105r.status == "PROVED_LOCALLY"
        and t106.status == "PROVED_LOCALLY"
        and t107.status == "PROVED_LOCALLY"
        and t108.status == "PROVED_LOCALLY"
    )
    status: T101UStatus = "PROVED_LOCALLY" if finite_ok and infinite_ok else "CONJECTURAL_UNIVERSAL_EXHAUSTION"
    return T101UAugmentedCertificate(
        status=status,
        finite_domain=finite_ok,
        augmented_infinite=infinite_ok,
        messages=[
            f"finite={t101f.status}, t108={t108.status}, t105r={t105r.status}",
        ],
    )
