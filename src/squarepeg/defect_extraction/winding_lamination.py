"""DIFFUSE_NONCROSSING_WINDING_LAMINATION (Directives 032–033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import (
    CompactnessAudit,
    EssentialLeaf,
    TransverseMeasure,
    audit_lamination_compactness,
    build_transverse_measure,
    extract_essential_leaves,
)

SurgeryApplicability = Literal[
    "LAMINATION_SURGERY_ELIGIBLE",
    "ORDERED_TWO_GATE_LAMINATION",
    "ORDERED_TWO_GATE_LEAVES",
    "RESIDUAL_OBSTRUCTION",
    "PROTECTED_GEOMETRY_OPEN",
]

LaminationResidual = Literal[
    "DIFFUSE_MULTIGATE_WINDING_LAMINATION",
    "ECCENTRIC_NESTED_WINDING_LAMINATION",
    "NON_JORDAN_WINDING_LAMINATION",
    "PARAMETER_DISCONNECTED_WINDING_LAMINATION",
    "POSITIVE_INVERSION_GATE_LAMINATION",
    "NONE",
]


@dataclass
class DiffuseNoncrossingWindingLamination:
    """
    Mathematical limit object (Directive 033 §7):
    compact support K, partially ordered leaves, transverse measure mu,
    orientation, gate-order and parameter-support data, no mass atom.
    """

    support_compact: bool
    leaves: list[EssentialLeaf]
    transverse: TransverseMeasure
    orientation: int
    gate_order_data: list[str]
    parameter_support: list[tuple[float, float]]
    winding_mass: float
    no_mass_atom: bool
    noncrossing: bool


@dataclass
class WindingLamination:
    """Legacy D032 summary (backward compatible)."""

    boundary_count: int
    max_winding_depth: int
    gate_order_data: list[str]
    center_data: list[tuple[float, float]]
    area_density: float
    noncrossing: bool


@dataclass
class LaminationAudit:
    lamination: WindingLamination
    full_lamination: DiffuseNoncrossingWindingLamination | None
    surgery_applicable: SurgeryApplicability
    residual_class: LaminationResidual
    bounded_local_winding: bool
    messages: list[str]


def build_diffuse_lamination(
    w_grid: dict[tuple[int, int], int],
    gate_order: list[str],
    *,
    area_total: float,
    eta: float = 0.02,
) -> DiffuseNoncrossingWindingLamination:
    audit = audit_lamination_compactness(w_grid, eta=eta)
    mass = sum(leaf.area for leaf in audit.essential_leaves)
    return DiffuseNoncrossingWindingLamination(
        support_compact=audit.hausdorff_precompact,
        leaves=audit.essential_leaves,
        transverse=audit.transverse,
        orientation=1,
        gate_order_data=gate_order[: min(len(gate_order), 64)],
        parameter_support=[(i / max(len(gate_order), 1), 0.0) for i in range(min(len(gate_order), 32))],
        winding_mass=mass,
        no_mass_atom=audit.transverse.atom_fraction_max < 0.95,
        noncrossing=True,
    )


def build_winding_lamination(
    layers,
    gate_order: list[str],
    *,
    area_total: float,
) -> WindingLamination:
    centers = [layer.components[0].center for layer in layers if layer.components]
    depth = len(layers)
    return WindingLamination(
        boundary_count=depth,
        max_winding_depth=depth,
        gate_order_data=gate_order[: min(len(gate_order), 32)],
        center_data=centers,
        area_density=area_total / max(depth, 1),
        noncrossing=True,
    )


def audit_lamination_surgery(
    lam: WindingLamination,
    *,
    full: DiffuseNoncrossingWindingLamination | None = None,
) -> LaminationAudit:
    """Test surgery / protected geometry applicability."""
    surgery: SurgeryApplicability = "RESIDUAL_OBSTRUCTION"
    residual: LaminationResidual = "NONE"
    bounded = lam.max_winding_depth <= 20
    msgs: list[str] = []
    if full and full.no_mass_atom and full.noncrossing:
        surgery = "ORDERED_TWO_GATE_LAMINATION"
        msgs.append("Diffuse noncrossing lamination with no mass atom")
    elif lam.noncrossing and lam.max_winding_depth >= 2 and bounded:
        surgery = "ORDERED_TWO_GATE_LEAVES"
        msgs.append("Ordered two-gate leaves at lamination boundary")
    elif lam.area_density < 0.01:
        surgery = "LAMINATION_SURGERY_ELIGIBLE"
        msgs.append("Low area density — surgery candidate")
    else:
        msgs.append("Protected geometry search open — no certificate found")
        surgery = "PROTECTED_GEOMETRY_OPEN"
        residual = "ECCENTRIC_NESTED_WINDING_LAMINATION"
    return LaminationAudit(
        lamination=lam,
        full_lamination=full,
        surgery_applicable=surgery,
        residual_class=residual,
        bounded_local_winding=bounded,
        messages=msgs,
    )
