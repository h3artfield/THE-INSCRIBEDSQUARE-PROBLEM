"""T089E — Coherent empty-core singleton reduction (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.t103_coherent_route import certify_t103_coherent
from squarepeg.defect_extraction.t108_exhaustion import certify_t108
from squarepeg.defect_extraction.universal_empty_neutral_core import certify_t102u_augmented

T089EStatus = Literal["CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY"]
GlobalResidual = Literal[
    "INFINITE_CENTER_GEOMETRY",
    "PARAMETER_DISCONNECTED_LIMIT",
    "NON_JORDAN_SATURATION_HULL",
    "POSITIVE_SCALE_NONANNULAR_CLUSTER",
    "NONSUMMABLE_DIFFUSE_END_GEOMETRY",
    "NONE",
]


@dataclass
class T089ECoherentCertificate:
    status: T089EStatus
    neutral_residual_eliminated: bool
    global_residual: GlobalResidual
    messages: list[str]


def certify_t089e_coherent(tree: CanonicalIntrusionTree) -> T089ECoherentCertificate:
    t108 = certify_t108(tree)
    t102u = certify_t102u_augmented(tree)
    t103 = certify_t103_coherent(tree)
    residual: GlobalResidual = "NONE"
    if t103.outcome == "COHERENT_GLOBAL_RESIDUAL":
        residual = "POSITIVE_SCALE_NONANNULAR_CLUSTER"
    eliminated = (
        t108.status == "PROVED_LOCALLY"
        and t102u.status == "PROVED_LOCALLY"
        and t103.status == "PROVED_LOCALLY"
    )
    status: T089EStatus = "PROVED_LOCALLY" if eliminated else "CONJECTURAL_REDUCTION_TARGET"
    return T089ECoherentCertificate(
        status=status,
        neutral_residual_eliminated=eliminated,
        global_residual=residual,
        messages=[f"t108={t108.status}, t102u={t102u.status}, t103={t103.status}"],
    )
