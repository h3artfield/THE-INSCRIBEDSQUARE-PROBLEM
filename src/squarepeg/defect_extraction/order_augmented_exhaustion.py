"""T108 — Order-augmented infinite transition exhaustion (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.countable_child_transition_routes import certify_t104
from squarepeg.defect_extraction.t105r_measure_closure import certify_t105r
from squarepeg.defect_extraction.unbounded_gate_transition_routes import certify_t106
from squarepeg.defect_extraction.universal_infinite_transition_exhaustion import certify_t101u

T108Status = Literal["CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T108Certificate:
    status: T108Status
    t104_revalidated: bool
    t106_revalidated: bool
    residual_empty: bool
    messages: list[str]


def certify_t108(tree: CanonicalIntrusionTree) -> T108Certificate:
    t104 = certify_t104(tree)
    t106 = certify_t106(tree)
    t105r = certify_t105r(tree)
    t101u = certify_t101u(tree)
    re104 = t104.status == "PROVED_LOCALLY"
    re106 = t106.status == "PROVED_LOCALLY"
    empty = t105r.status == "PROVED_LOCALLY" and t101u.status == "PROVED_LOCALLY"
    status: T108Status = "PROVED_LOCALLY" if empty else "CONJECTURAL_EXHAUSTION_TARGET"
    return T108Certificate(status, re104, re106, empty, [f"t105r={t105r.status}, t101u={t101u.status}"])
