"""T061R and T065 finite dense-gate reduction (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.concentration_compactness import classify_concentration_compactness
from squarepeg.defect_extraction.concentrated_parameter_block import extract_consecutive_block
from squarepeg.defect_extraction.dense_normalization import DenseClusterRecord, normalize_dense_cluster
from squarepeg.defect_extraction.diffuse_winding_layers import audit_diffuse_layers
from squarepeg.defect_extraction.finite_center_extraction import certify_t062_complete
from squarepeg.defect_extraction.recursive_dense_descent import recursive_dense_descent
from squarepeg.defect_extraction.winding_function import split_winding_mass, winding_grid, winding_l_infinity_lower
from squarepeg.defect_extraction.winding_layers import build_winding_layers, layer_cake_identity_holds
from squarepeg.defect_extraction.winding_lamination import audit_lamination_surgery, build_winding_lamination
from squarepeg.defect_extraction.winding_layer_tree import build_layer_tree

T061RBranch = Literal[
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_DECOMPOSITION",
    "DIFFUSE_NESTED_LAYERS",
    "DISCONNECTED_OR_NONJORDAN",
]

T065Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_REDUCTION"]
T065Outcome = Literal[
    "SIGNATURE_CONTROLLED_SURGERY",
    "INFINITE_INTRUSION_RAY",
    "DIFFUSE_WINDING_LAMINATION",
    "NON_JORDAN_HULL",
    "POSITIVE_SCALE_NONANNULAR",
]


@dataclass
class T061RAudit:
    branch: T061RBranch
    t063_regime: str
    messages: list[str]


@dataclass
class T065Certificate:
    status: T065Status
    outcome: T065Outcome
    t061r: T061RAudit
    finite_tree_eliminated: bool
    messages: list[str]


def audit_t061r(
    record: DenseClusterRecord,
    attachment_chain: list[tuple[float, float]],
    gate_ids: list[str],
    param_order: list[int],
    gate_points: list[tuple[float, float]],
) -> T061RAudit:
    """T061R: winding-layer refinement of T061."""
    norm = normalize_dense_cluster(record, gate_points, attachment_chain)
    w = winding_grid(attachment_chain if attachment_chain else [(0, 0), (0.5, 0.5), (1, 0)])
    mass = split_winding_mass(w)
    t063 = classify_concentration_compactness(w, mass)
    branch: T061RBranch = "DIFFUSE_NESTED_LAYERS"
    msgs = list(t063.messages)
    if t063.regime == "CONCENTRATED":
        ext = extract_consecutive_block(
            gate_ids, param_order, [record.area_absolute / max(len(gate_ids), 1)] * len(gate_ids),
            gate_points, center=record.center, rho=0.2, r=record.diameter_r,
        )
        branch = "CONCENTRATED_DESCENT" if ext.block else "DISCONNECTED_OR_NONJORDAN"
        if ext.spatial_only:
            branch = "DISCONNECTED_OR_NONJORDAN"
    elif t063.regime == "MULTICENTER":
        branch = "FINITE_CENTER_DECOMPOSITION"
    else:
        layers = build_winding_layers(w)
        audit_diffuse_layers(layers)
        branch = "DIFFUSE_NESTED_LAYERS"
    return T061RAudit(branch=branch, t063_regime=t063.regime, messages=msgs)


def certify_t065(
    record: DenseClusterRecord,
    attachment_chain: list[tuple[float, float]],
    gate_ids: list[str],
    param_order: list[int],
    gate_points: list[tuple[float, float]],
    *,
    k: int = 3,
) -> T065Certificate:
    """T065: every dense-gate finite-intrusion sequence reduces to known residual."""
    t061r = audit_t061r(record, attachment_chain, gate_ids, param_order, gate_points)
    outcome: T065Outcome = "DIFFUSE_WINDING_LAMINATION"
    status: T065Status = "CONJECTURAL_TARGET"
    msgs = list(t061r.messages)
    if t061r.branch == "CONCENTRATED_DESCENT":
        descent = recursive_dense_descent(
            [record],
            [gate_ids],
            [param_order],
            [[record.area_absolute / max(len(gate_ids), 1)] * len(gate_ids)],
            [gate_points],
        )
        if descent.fixed_defect_preserved:
            outcome = "INFINITE_INTRUSION_RAY"
            status = "PROVED_LOCALLY_REDUCTION"
            msgs.append("Concentrated descent to intrusion ray")
    elif t061r.branch == "FINITE_CENTER_DECOMPOSITION":
        t062 = certify_t062_complete(gate_points, gate_ids, k=k, r=record.diameter_r)
        if t062.extraction_via_t053b:
            outcome = "SIGNATURE_CONTROLLED_SURGERY"
            status = "PROVED_LOCALLY_REDUCTION"
            msgs.append("T062 finite-center extraction")
    elif t061r.branch == "DIFFUSE_NESTED_LAYERS":
        w = winding_grid(attachment_chain or [(0, 0), (0.3, 0.4), (0.6, 0.2), (0, 0)])
        layers = build_winding_layers(w)
        lam = build_winding_lamination(layers, gate_ids, area_total=record.area_absolute)
        la = audit_lamination_surgery(lam)
        outcome = "DIFFUSE_WINDING_LAMINATION"
        msgs.extend(la.messages)
    if record.diameter_r > 0.4:
        outcome = "POSITIVE_SCALE_NONANNULAR"
    eliminated = outcome in ("SIGNATURE_CONTROLLED_SURGERY", "INFINITE_INTRUSION_RAY")
    return T065Certificate(
        status=status,
        outcome=outcome,
        t061r=t061r,
        finite_tree_eliminated=eliminated,
        messages=msgs,
    )
