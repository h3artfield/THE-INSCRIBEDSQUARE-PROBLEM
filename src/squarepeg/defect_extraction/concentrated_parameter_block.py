"""Consecutive parameter block extraction (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass

Point = tuple[float, float]


@dataclass
class ParameterBlock:
    block_id: str
    gate_ids: list[str]
    param_indices: list[int]
    attachment_area: float
    spatial_diameter_normalized: float
    consecutive: bool


@dataclass
class BlockExtractionAudit:
    block: ParameterBlock | None
    defect_fraction: float
    original_scale_diameter: float
    parameter_consecutive: bool
    spatial_only: bool
    messages: list[str]


def extract_consecutive_block(
    gate_ids: list[str],
    param_order: list[int],
    attachment_per_gate: list[float],
    gate_positions: list[Point],
    *,
    center: Point,
    rho: float,
    r: float,
    epsilon: float = 0.025,
    c1: float = 0.25,
    window: int = 4,
) -> BlockExtractionAudit:
    """
    Identify consecutive parameter/gate block in B(x_n, C rho) with |A_B| >= c1 epsilon.

    Distinguishes parameter-consecutive from spatial-only concentration.
    """
    if not gate_ids or not attachment_per_gate:
        return BlockExtractionAudit(None, 0.0, 0.0, False, False, ["Empty"])
    best_mass = 0.0
    best_start = 0
    for i in range(len(gate_ids) - window + 1):
        mass = abs(sum(attachment_per_gate[i : i + window]))
        if mass > best_mass:
            best_mass = mass
            best_start = i
    chunk_ids = gate_ids[best_start : best_start + window]
    chunk_params = param_order[best_start : best_start + window] if param_order else list(range(best_start, best_start + window))
    consecutive = chunk_params == sorted(chunk_params) or max(chunk_params) - min(chunk_params) == window - 1
    pts = gate_positions[best_start : best_start + window] if len(gate_positions) >= best_start + window else []
    diam_norm = 0.0
    if pts:
        cx, cy = center
        diam_norm = max((((p[0] - cx) ** 2 + (p[1] - cy) ** 2) ** 0.5 for p in pts), default=0.0)
    in_ball = diam_norm <= rho * 2
    spatial_only = in_ball and not consecutive
    block = ParameterBlock(
        block_id=f"B{best_start}",
        gate_ids=chunk_ids,
        param_indices=chunk_params,
        attachment_area=best_mass,
        spatial_diameter_normalized=diam_norm,
        consecutive=consecutive and in_ball,
    )
    frac = best_mass / epsilon if epsilon > 0 else 0.0
    return BlockExtractionAudit(
        block=block if frac >= c1 else None,
        defect_fraction=frac,
        original_scale_diameter=r * diam_norm,
        parameter_consecutive=consecutive,
        spatial_only=spatial_only,
        messages=[f"Block fraction={frac:.3f}, consecutive={consecutive}"],
    )
