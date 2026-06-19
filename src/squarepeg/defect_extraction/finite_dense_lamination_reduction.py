"""T065R finite dense-tree lamination reduction (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.annular_band_extraction import certify_t067
from squarepeg.defect_extraction.dense_normalization import DenseClusterRecord, normalize_dense_cluster
from squarepeg.defect_extraction.disconnected_concentration import certify_t064d
from squarepeg.defect_extraction.finite_center_extraction import certify_t062_complete
from squarepeg.defect_extraction.ordered_leaf_surgery import certify_t066
from squarepeg.defect_extraction.recursive_dense_descent import recursive_dense_descent
from squarepeg.defect_extraction.winding_function import winding_grid
from squarepeg.defect_extraction.winding_layers import build_winding_layers
from squarepeg.defect_extraction.winding_lamination import (
    LaminationResidual,
    build_diffuse_lamination,
    build_winding_lamination,
)

T065RStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T065ROutcome = Literal[
    "SIGNATURE_CONTROLLED_SURGERY",
    "RECURSIVE_CONCENTRATED_DESCENT",
    "FINITE_CENTER_REDUCTION",
    "ORDERED_TWO_GATE_LAMINATION_SURGERY",
    "PROTECTED_ANNULAR_GEOMETRY",
    "EXPLICIT_LAMINATION_RESIDUAL",
    "NON_JORDAN_SATURATION_HULL",
]


@dataclass
class T065RCertificate:
    status: T065RStatus
    outcome: T065ROutcome
    residual_class: LaminationResidual
    finite_dense_eliminated: bool
    t066_proved: bool
    t067_proved: bool
    t064d_closed: bool
    messages: list[str]


def certify_t065r(
    record: DenseClusterRecord,
    attachment_chain: list[tuple[float, float]],
    gate_ids: list[str],
    param_order: list[int],
    gate_points: list[tuple[float, float]],
    *,
    k: int = 4,
) -> T065RCertificate:
    """T065R: finite dense-tree lamination reduction."""
    att = [record.area_absolute / max(len(gate_ids), 1)] * len(gate_ids)
    t064d = certify_t064d(
        gate_ids,
        param_order,
        att,
        gate_points,
        attachment_chain,
        center=record.center,
        r=record.diameter_r,
        epsilon=record.area_absolute,
        k_centers=k,
    )
    w = winding_grid(attachment_chain or [(0, 0), (0.4, 0.3), (0.7, 0.1), (0, 0)])
    layers = build_winding_layers(w)
    full_lam = build_diffuse_lamination(w, gate_ids, area_total=record.area_absolute)
    lam = build_winding_lamination(layers, gate_ids, area_total=record.area_absolute)
    t066 = certify_t066(full_lam)
    t067 = certify_t067(full_lam, layers)
    outcome: T065ROutcome = "EXPLICIT_LAMINATION_RESIDUAL"
    residual: LaminationResidual = "NONE"
    status: T065RStatus = "CONJECTURAL_TARGET"
    msgs = list(t064d.messages)
    if t064d.outcome == "PARAMETER_CONSECUTIVE_BLOCK":
        descent = recursive_dense_descent(
            [record],
            [gate_ids],
            [param_order],
            [att],
            [gate_points],
        )
        if descent.fixed_defect_preserved:
            outcome = "RECURSIVE_CONCENTRATED_DESCENT"
            status = "PROVED_LOCALLY_PARTIAL"
    elif t064d.outcome == "FINITE_CENTER_T062":
        t062 = certify_t062_complete(gate_points, gate_ids, k=k, r=record.diameter_r)
        if t062.extraction_via_t053b:
            outcome = "FINITE_CENTER_REDUCTION"
            status = "PROVED_LOCALLY_PARTIAL"
            msgs.append("T062 finite-center")
    elif t066.status == "PROVED_LOCALLY":
        outcome = "ORDERED_TWO_GATE_LAMINATION_SURGERY"
        status = "PROVED_LOCALLY_PARTIAL"
        msgs.append("T066 ordered lamination surgery")
    elif t067.status == "PROVED_LOCALLY" and t067.outcome == "ANNULAR_BAND_CERTIFIED":
        outcome = "PROTECTED_ANNULAR_GEOMETRY"
        status = "PROVED_LOCALLY_PARTIAL"
        msgs.append("T067 annular band")
    elif t067.outcome == "ORDERED_TWO_GATE_MASS" and t066.is_ordered_two_gate:
        outcome = "ORDERED_TWO_GATE_LAMINATION_SURGERY"
        status = "PROVED_LOCALLY_PARTIAL"
    else:
        if not full_lam.no_mass_atom:
            residual = "DIFFUSE_MULTIGATE_WINDING_LAMINATION"
        elif t064d.disconnected:
            residual = "PARAMETER_DISCONNECTED_WINDING_LAMINATION"
        else:
            residual = "ECCENTRIC_NESTED_WINDING_LAMINATION"
        outcome = "EXPLICIT_LAMINATION_RESIDUAL"
        msgs.append(f"Residual: {residual}")
    if record.diameter_r > 0.4:
        outcome = "NON_JORDAN_SATURATION_HULL" if not lam.noncrossing else outcome
    eliminated = outcome in (
        "SIGNATURE_CONTROLLED_SURGERY",
        "RECURSIVE_CONCENTRATED_DESCENT",
        "FINITE_CENTER_REDUCTION",
        "ORDERED_TWO_GATE_LAMINATION_SURGERY",
        "PROTECTED_ANNULAR_GEOMETRY",
    )
    return T065RCertificate(
        status=status,
        outcome=outcome,
        residual_class=residual,
        finite_dense_eliminated=eliminated,
        t066_proved=t066.status == "PROVED_LOCALLY",
        t067_proved=t067.status == "PROVED_LOCALLY",
        t064d_closed=t064d.status == "PROVED_LOCALLY",
        messages=msgs,
    )
