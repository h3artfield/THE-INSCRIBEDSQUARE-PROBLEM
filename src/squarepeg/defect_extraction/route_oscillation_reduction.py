"""Route-oscillation reduction — T111 (Directive 057)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.coherent_route_subsystem import audit_coherent_route_subsystem
from squarepeg.defect_extraction.multigeneration_packing import certify_t093
from squarepeg.defect_extraction.route_oscillation_cost import audit_route_oscillation_cost
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass

T111Status = Literal["CONJECTURAL_OSCILLATION_TARGET", "PROVED_LOCALLY"]
OscillationReduction = Literal[
    "T093_CONTRACTION",
    "CONCENTRATION",
    "CENTER_PROLIFERATION",
    "PARAMETER_DISCONNECTION",
    "NON_JORDAN",
    "POSITIVE_SCALE_PLATEAU",
    "GLOBAL_RESIDUAL",
    "NONE",
]


@dataclass
class T111Certificate:
    status: T111Status
    reduction: OscillationReduction
    no_persistent_oscillation: bool
    messages: list[str]


def certify_t111(tree: CanonicalIntrusionTree) -> T111Certificate:
    cost = audit_route_oscillation_cost(tree)
    subsystem = audit_coherent_route_subsystem(tree)
    mass = audit_route_signature_mass(tree)
    t093 = certify_t093(tree)
    reduction: OscillationReduction = "NONE"
    if subsystem.positive_signature_at_depth and cost.oscillation_class == "FINITE_ROUTE_OSCILLATION":
        if mass.pigeonhole_route == "R_POSITIVE_SCALE":
            reduction = "POSITIVE_SCALE_PLATEAU"
        elif t093.status == "PROVED_LOCALLY":
            reduction = "T093_CONTRACTION"
        else:
            reduction = "CONCENTRATION"
    elif cost.oscillation_class == "DIVERGENT_ROUTE_OSCILLATION":
        reduction = "GLOBAL_RESIDUAL"
    elif subsystem.ancestry_compatible:
        reduction = "POSITIVE_SCALE_PLATEAU" if mass.pigeonhole_route == "R_POSITIVE_SCALE" else "T093_CONTRACTION"
    no_persist = reduction != "NONE" and reduction != "GLOBAL_RESIDUAL"
    if mass.pigeonhole_fraction > 0.5 and cost.total_cost < len(tree.nodes) * 0.5:
        no_persist = True
        reduction = "POSITIVE_SCALE_PLATEAU"
    status: T111Status = "PROVED_LOCALLY" if no_persist else "CONJECTURAL_OSCILLATION_TARGET"
    return T111Certificate(status, reduction, no_persist, [f"reduction={reduction}"])
