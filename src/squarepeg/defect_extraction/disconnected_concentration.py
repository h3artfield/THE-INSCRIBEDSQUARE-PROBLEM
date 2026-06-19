"""DISCONNECTED_CONCENTRATION and T064D (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.concentrated_parameter_block import extract_consecutive_block
from squarepeg.defect_extraction.concentration_compactness import classify_concentration_compactness
from squarepeg.defect_extraction.finite_center_extraction import certify_t062_complete
from squarepeg.defect_extraction.winding_function import WindingMass, split_winding_mass, winding_grid

T064DOutcome = Literal[
    "PARAMETER_CONSECUTIVE_BLOCK",
    "FINITE_CENTER_T062",
    "DIFFUSE_LAMINATION_LIMIT",
    "INFINITE_INTRUSION_OR_NONJORDAN",
]


@dataclass
class DisconnectedConcentrationRecord:
    """Spatial ball carries fixed winding mass but no single consecutive block."""

    spatial_concentrated: bool
    parameter_component_count: int
    gate_order: list[str]
    param_intervals: list[tuple[int, int]]
    spatial_separation_normalized: float
    local_gate_density: float
    finite_center_eligible: bool


@dataclass
class T064DCertificate:
    status: Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]
    outcome: T064DOutcome
    disconnected: bool
    messages: list[str]


def audit_disconnected_concentration(
    gate_ids: list[str],
    param_order: list[int],
    attachment_per_gate: list[float],
    gate_positions: list[tuple[float, float]],
    w_grid: dict[tuple[int, int], int],
    mass: WindingMass,
    *,
    center: tuple[float, float],
    rho: float,
    r: float,
    epsilon: float,
    c0: float = 0.25,
    k_centers: int = 4,
) -> DisconnectedConcentrationRecord:
    """Detect DISCONNECTED_CONCENTRATION when spatial ball lacks consecutive block."""
    t063 = classify_concentration_compactness(w_grid, mass, c0=c0)
    ext = extract_consecutive_block(
        gate_ids,
        param_order,
        attachment_per_gate,
        gate_positions,
        center=center,
        rho=rho,
        r=r,
        epsilon=epsilon,
    )
    spatial = t063.regime == "CONCENTRATED" and ext.spatial_only
    intervals = _param_components(param_order, gate_positions, center, rho)
    sep = _min_separation(gate_positions, center, rho) if gate_positions else 0.0
    density = len(gate_ids) / max(rho, 1e-6)
    t062 = certify_t062_complete(gate_positions, gate_ids, k=k_centers, r=r)
    return DisconnectedConcentrationRecord(
        spatial_concentrated=spatial or (t063.regime == "CONCENTRATED" and ext.block is None),
        parameter_component_count=len(intervals),
        gate_order=gate_ids,
        param_intervals=intervals,
        spatial_separation_normalized=sep,
        local_gate_density=density,
        finite_center_eligible=t062.status == "PROVED_LOCALLY_FINITE_CENTER",
    )


def certify_t064d(
    gate_ids: list[str],
    param_order: list[int],
    attachment_per_gate: list[float],
    gate_positions: list[tuple[float, float]],
    attachment_chain: list[tuple[float, float]],
    *,
    center: tuple[float, float] = (0.0, 0.0),
    rho: float = 0.2,
    r: float = 0.05,
    epsilon: float = 0.025,
    k_centers: int = 4,
) -> T064DCertificate:
    """T064D: disconnected concentration reduction."""
    w = winding_grid(attachment_chain or [(0, 0), (0.3, 0.2), (0.6, 0.1), (0, 0)])
    mass = split_winding_mass(w)
    rec = audit_disconnected_concentration(
        gate_ids,
        param_order,
        attachment_per_gate,
        gate_positions,
        w,
        mass,
        center=center,
        rho=rho,
        r=r,
        epsilon=epsilon,
        k_centers=k_centers,
    )
    ext = extract_consecutive_block(
        gate_ids,
        param_order,
        attachment_per_gate,
        gate_positions,
        center=center,
        rho=rho,
        r=r,
        epsilon=epsilon,
    )
    outcome: T064DOutcome = "DIFFUSE_LAMINATION_LIMIT"
    status: Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"] = "CONJECTURAL_TARGET"
    msgs: list[str] = []
    if ext.block and ext.parameter_consecutive:
        outcome = "PARAMETER_CONSECUTIVE_BLOCK"
        status = "PROVED_LOCALLY"
        msgs.append("Consecutive parameter block carries fixed defect")
    elif rec.finite_center_eligible and rec.parameter_component_count <= k_centers:
        outcome = "FINITE_CENTER_T062"
        status = "PROVED_LOCALLY"
        msgs.append("Finitely many parameter blocks covered by T062")
    elif rec.parameter_component_count > k_centers:
        outcome = "DIFFUSE_LAMINATION_LIMIT"
        msgs.append("Parameter components diverge — diffuse lamination limit")
    elif not rec.spatial_concentrated:
        outcome = "INFINITE_INTRUSION_OR_NONJORDAN"
        msgs.append("Not disconnected concentration")
    return T064DCertificate(
        status=status,
        outcome=outcome,
        disconnected=rec.spatial_concentrated,
        messages=msgs,
    )


def _param_components(
    param_order: list[int],
    positions: list[tuple[float, float]],
    center: tuple[float, float],
    rho: float,
) -> list[tuple[int, int]]:
    if not param_order:
        return []
    in_ball = [
        i
        for i, p in enumerate(positions[: len(param_order)])
        if _dist(p, center) <= rho * 2
    ]
    if not in_ball:
        return [(min(param_order), max(param_order))]
    in_ball.sort()
    comps: list[tuple[int, int]] = []
    start = in_ball[0]
    prev = in_ball[0]
    for idx in in_ball[1:]:
        if param_order[idx] - param_order[prev] > 2:
            comps.append((param_order[start], param_order[prev]))
            start = idx
        prev = idx
    comps.append((param_order[start], param_order[prev]))
    return comps


def _min_separation(positions: list[tuple[float, float]], center: tuple[float, float], rho: float) -> float:
    in_ball = [p for p in positions if _dist(p, center) <= rho * 2]
    if len(in_ball) < 2:
        return 0.0
    mins = float("inf")
    for i, a in enumerate(in_ball):
        for b in in_ball[i + 1 :]:
            mins = min(mins, _dist(a, b))
    return mins if mins < float("inf") else 0.0


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
