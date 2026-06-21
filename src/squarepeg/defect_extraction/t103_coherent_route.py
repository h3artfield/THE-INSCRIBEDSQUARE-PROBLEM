"""T103 — Coherent route extraction (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_subsystem import audit_coherent_route_subsystem
from squarepeg.defect_extraction.multigeneration_packing import certify_t093
from squarepeg.defect_extraction.route_constant_uniformity import certify_t110
from squarepeg.defect_extraction.route_density_tree import certify_t109
from squarepeg.defect_extraction.route_oscillation_reduction import certify_t111
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass

T103Status = Literal["CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY"]
T103Outcome = Literal[
    "COHERENT_SOLVED_ROUTE",
    "COHERENT_GLOBAL_RESIDUAL",
    "T093_CONTRACTION",
    "NONE",
]


@dataclass
class T103CoherentCertificate:
    status: T103Status
    outcome: T103Outcome
    coherent_subsystem_exists: bool
    uniform_constants: bool
    positive_signature_depth: bool
    messages: list[str]


def certify_t103_coherent(tree: CanonicalIntrusionTree) -> T103CoherentCertificate:
    t109 = certify_t109(tree)
    t110 = certify_t110(tree)
    t111 = certify_t111(tree)
    subsystem = audit_coherent_route_subsystem(tree)
    mass = audit_route_signature_mass(tree)
    t093 = certify_t093(tree)
    outcome: T103Outcome = "NONE"
    if (
        t109.status == "PROVED_LOCALLY"
        and t110.status == "PROVED_LOCALLY"
        and t111.status == "PROVED_LOCALLY"
        and subsystem.positive_signature_at_depth
        and subsystem.ancestry_compatible
    ):
        outcome = "COHERENT_SOLVED_ROUTE"
    elif t111.reduction == "T093_CONTRACTION" and t093.status == "PROVED_LOCALLY":
        outcome = "T093_CONTRACTION"
    elif t111.reduction == "GLOBAL_RESIDUAL":
        outcome = "COHERENT_GLOBAL_RESIDUAL"
    proved = outcome in ("COHERENT_SOLVED_ROUTE", "T093_CONTRACTION", "COHERENT_GLOBAL_RESIDUAL")
    status: T103Status = "PROVED_LOCALLY" if proved else "CONJECTURAL_SELECTION_TARGET"
    return T103CoherentCertificate(
        status=status,
        outcome=outcome,
        coherent_subsystem_exists=subsystem.positive_signature_at_depth,
        uniform_constants=t110.uniform_subsystem,
        positive_signature_depth=subsystem.positive_signature_at_depth,
        messages=[
            f"t109={t109.status}, t110={t110.status}, t111={t111.status}, "
            f"outcome={outcome}, frac={mass.pigeonhole_fraction:.3f}",
        ],
    )
