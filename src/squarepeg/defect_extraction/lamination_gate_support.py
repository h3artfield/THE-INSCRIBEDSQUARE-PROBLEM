"""Parameter support S_L for lamination leaves (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ParameterSupportClass = Literal[
    "ONE_INTERVAL",
    "FINITELY_MANY_INTERVALS",
    "CANTOR_TYPE",
    "DENSE_IN_SUBINTERVAL",
]


@dataclass
class ParameterSupport:
    leaf_id: str
    support_class: ParameterSupportClass
    intervals: list[tuple[float, float]]
    cantor_like: bool
    surgery_compatible: bool


def classify_parameter_support(
    leaf_id: str,
    param_indices: list[int],
    *,
    total_params: int = 100,
) -> ParameterSupport:
    """Classify S_L subset of S^1 (discretized)."""
    if not param_indices:
        return ParameterSupport(
            leaf_id=leaf_id,
            support_class="ONE_INTERVAL",
            intervals=[(0.0, 1.0)],
            cantor_like=False,
            surgery_compatible=True,
        )
    sorted_idx = sorted(set(param_indices))
    intervals: list[tuple[float, float]] = []
    start = sorted_idx[0]
    prev = sorted_idx[0]
    gap_threshold = max(2, total_params // 20)
    for idx in sorted_idx[1:]:
        if idx - prev > gap_threshold:
            intervals.append((start / total_params, prev / total_params))
            start = idx
        prev = idx
    intervals.append((start / total_params, prev / total_params))
    support: ParameterSupportClass = "ONE_INTERVAL"
    cantor = False
    if len(intervals) == 1:
        support = "ONE_INTERVAL"
    elif len(intervals) <= 5:
        support = "FINITELY_MANY_INTERVALS"
    elif len(intervals) > 10 and all(b - a < 0.05 for a, b in intervals):
        support = "CANTOR_TYPE"
        cantor = True
    else:
        support = "DENSE_IN_SUBINTERVAL"
    surgery = support in ("ONE_INTERVAL", "FINITELY_MANY_INTERVALS") and not cantor
    return ParameterSupport(
        leaf_id=leaf_id,
        support_class=support,
        intervals=intervals,
        cantor_like=cantor,
        surgery_compatible=surgery,
    )
