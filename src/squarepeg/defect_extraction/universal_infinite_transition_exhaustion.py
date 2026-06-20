"""T101-U / T102-U universal infinite transition exhaustion (Directive 054)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.countable_child_transition_routes import certify_t104
from squarepeg.defect_extraction.empty_neutral_core import certify_t102
from squarepeg.defect_extraction.measure_transition_closure import certify_t105
from squarepeg.defect_extraction.unbounded_gate_transition_routes import certify_t106
from squarepeg.defect_extraction.universal_transition_exhaustion import certify_t101

T101UStatus = Literal["CONJECTURAL_UNIVERSAL_EXHAUSTION", "PROVED_LOCALLY"]
T102UStatus = Literal["CONJECTURAL_UNIVERSAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T101UCertificate:
    status: T101UStatus
    finite_domain: bool
    infinite_branches: bool
    messages: list[str]


@dataclass
class T102UCertificate:
    status: T102UStatus
    residual_empty: bool
    global_residuals_named: bool
    messages: list[str]


def certify_t101u(tree: CanonicalIntrusionTree) -> T101UCertificate:
    t101f = certify_t101(tree)
    t104 = certify_t104(tree)
    t105 = certify_t105(tree)
    t106 = certify_t106(tree)
    infinite_ok = (
        t104.status == "PROVED_LOCALLY"
        and t105.status == "PROVED_LOCALLY"
        and t106.status == "PROVED_LOCALLY"
    )
    if t101f.status == "PROVED_FINITE_DOMAIN" and infinite_ok:
        status: T101UStatus = "PROVED_LOCALLY"
    else:
        status = "CONJECTURAL_UNIVERSAL_EXHAUSTION"
    return T101UCertificate(
        status,
        t101f.status == "PROVED_FINITE_DOMAIN",
        infinite_ok,
        [f"finite={t101f.status}, t104={t104.status}, t105={t105.status}, t106={t106.status}"],
    )


def certify_t102u(tree: CanonicalIntrusionTree) -> T102UCertificate:
    t101u = certify_t101u(tree)
    t102f = certify_t102(tree)
    if t101u.status == "PROVED_LOCALLY" and t102f.core_empty:
        status: T102UStatus = "PROVED_LOCALLY"
    else:
        status = "CONJECTURAL_UNIVERSAL_CORE_TARGET"
    return T102UCertificate(
        status,
        t102f.core_empty and t101u.status == "PROVED_LOCALLY",
        True,
        [f"t101u={t101u.status}, core_empty={t102f.core_empty}"],
    )
