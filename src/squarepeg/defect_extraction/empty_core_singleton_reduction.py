"""T089E — Empty-core singleton-end reduction (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_extraction import certify_t103
from squarepeg.defect_extraction.empty_neutral_core import certify_t102
from squarepeg.defect_extraction.universal_transition_exhaustion import certify_t101

T089EStatus = Literal["CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY"]
GlobalResidual = Literal[
    "INFINITE_CENTER",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "POSITIVE_SCALE_NONANNULAR",
    "NONE",
]


@dataclass
class T089ECertificate:
    status: T089EStatus
    neutral_residual_eliminated: bool
    global_residual: GlobalResidual
    messages: list[str]


def certify_t089e(tree: CanonicalIntrusionTree) -> T089ECertificate:
    t101 = certify_t101(tree)
    t102 = certify_t102(tree)
    t103 = certify_t103(tree)
    residual: GlobalResidual = "NONE"
    if t101.status == "CONJECTURAL_EXHAUSTION_TARGET":
        residual = "POSITIVE_SCALE_NONANNULAR"
    eliminated = (
        t102.status == "PROVED_LOCALLY"
        and t103.status == "PROVED_LOCALLY"
        and t101.status == "PROVED_LOCALLY"
    )
    status: T089EStatus = "PROVED_LOCALLY" if eliminated else "CONJECTURAL_REDUCTION_TARGET"
    return T089ECertificate(status, eliminated, residual, [f"t101={t101.status}, t102={t102.status}, t103={t103.status}"])
