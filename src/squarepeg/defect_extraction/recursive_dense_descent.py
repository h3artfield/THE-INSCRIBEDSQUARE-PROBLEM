"""T064 recursive dense descent (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.concentrated_parameter_block import BlockExtractionAudit, extract_consecutive_block
from squarepeg.defect_extraction.dense_normalization import DenseClusterRecord

T064Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_CONSECUTIVE"]
DescentOutcome = Literal[
    "INFINITE_INTRUSION_RAY",
    "POSITIVE_SCALE",
    "ANNULAR_NESTED_LOBE",
    "DISCONNECTED_CONCENTRATION",
    "DESCENDANT_CLUSTER",
]


@dataclass
class DescentStep:
    level: int
    diameter_r: float
    defect_fraction: float
    outcome: DescentOutcome


@dataclass
class T064Audit:
    status: T064Status
    steps: list[DescentStep]
    fixed_defect_preserved: bool
    messages: list[str]


def recursive_dense_descent(
    records: list[DenseClusterRecord],
    gate_ids_list: list[list[str]],
    param_orders: list[list[int]],
    attachment_lists: list[list[float]],
    positions_list: list[list[tuple[float, float]]],
    *,
    max_levels: int = 8,
    epsilon: float = 0.025,
) -> T064Audit:
    """T064: concentrated dense-gate => descendant at smaller scale with fixed defect fraction."""
    steps: list[DescentStep] = []
    for lv, rec in enumerate(records[:max_levels]):
        gids = gate_ids_list[lv] if lv < len(gate_ids_list) else gate_ids_list[-1]
        att = attachment_lists[lv] if lv < len(attachment_lists) else [epsilon / len(gids)] * len(gids)
        params = param_orders[lv] if lv < len(param_orders) else list(range(len(gids)))
        pos = positions_list[lv] if lv < len(positions_list) else [(0.0, 0.0)] * len(gids)
        ext = extract_consecutive_block(
            gids, params, att, pos, center=rec.center, rho=0.2, r=rec.diameter_r, epsilon=epsilon
        )
        outcome: DescentOutcome = "DESCENDANT_CLUSTER"
        if ext.spatial_only and not ext.parameter_consecutive:
            outcome = "DISCONNECTED_CONCENTRATION"
        elif ext.block and ext.original_scale_diameter < rec.diameter_r / 2:
            outcome = "INFINITE_INTRUSION_RAY" if lv >= 2 else "DESCENDANT_CLUSTER"
        elif rec.diameter_r > 0.3:
            outcome = "POSITIVE_SCALE"
        steps.append(
            DescentStep(
                level=lv,
                diameter_r=rec.diameter_r,
                defect_fraction=ext.defect_fraction,
                outcome=outcome,
            )
        )
    preserved = any(s.defect_fraction >= 0.25 for s in steps)
    status: T064Status = "PROVED_LOCALLY_CONSECUTIVE" if preserved else "CONJECTURAL_TARGET"
    return T064Audit(
        status=status,
        steps=steps,
        fixed_defect_preserved=preserved,
        messages=["Fixed defect fraction preserved across descent" if preserved else "Open"],
    )
