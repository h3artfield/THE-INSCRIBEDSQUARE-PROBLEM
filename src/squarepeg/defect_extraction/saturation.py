"""Intrusion saturation S_k(L) (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass, field

from squarepeg.defect_extraction.intrusion_noncrossing import IntrusionComponent

Point = tuple[float, float]


@dataclass
class SaturationState:
    lobe_id: str
    lobe_interval: tuple[float, float]
    level: int
    param_intervals: list[tuple[float, float]]
    intrusion_ids: list[str]
    stabilized: bool
    reaches_seam: bool


def one_step_saturation(
    lobe_interval: tuple[float, float],
    intrusions: list[IntrusionComponent],
) -> list[tuple[float, float]]:
    """S_1(L): full external parameter arcs supporting intrusions into Omega_L."""
    a, b = lobe_interval
    intervals = [lobe_interval]
    for k in intrusions:
        intervals.append(k.param_interval)
    return _merge_intervals(intervals)


def recursive_saturation(
    lobe_interval: tuple[float, float],
    intrusions: list[IntrusionComponent],
    *,
    max_depth: int = 16,
) -> SaturationState:
    """S_infty(L) via recursive absorption; detects finite stabilization."""
    current = one_step_saturation(lobe_interval, intrusions)
    seen = {tuple(current)}
    level = 1
    ids = [k.component_id for k in intrusions]
    while level < max_depth:
        expanded: list[tuple[float, float]] = list(current)
        for kid in intrusions:
            for child_id in kid.children:
                for other in intrusions:
                    if other.component_id == child_id:
                        expanded.append(other.param_interval)
        merged = _merge_intervals(expanded)
        key = tuple(merged)
        if key in seen:
            return SaturationState(
                lobe_id="L",
                lobe_interval=lobe_interval,
                level=level,
                param_intervals=merged,
                intrusion_ids=ids,
                stabilized=True,
                reaches_seam=_wraps_seam(merged),
            )
        seen.add(key)
        current = merged
        level += 1
    return SaturationState(
        lobe_id="L",
        lobe_interval=lobe_interval,
        level=level,
        param_intervals=current,
        intrusion_ids=ids,
        stabilized=False,
        reaches_seam=_wraps_seam(current),
    )


def saturation_order_independent(
    lobe_interval: tuple[float, float],
    intrusions: list[IntrusionComponent],
) -> bool:
    """Saturation result invariant under intrusion processing order."""
    a = recursive_saturation(lobe_interval, intrusions)
    b = recursive_saturation(lobe_interval, list(reversed(intrusions)))
    return tuple(a.param_intervals) == tuple(b.param_intervals)


def _merge_intervals(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if not intervals:
        return []
    pts = sorted(set(x for iv in intervals for x in iv))
    if len(pts) < 2:
        return intervals
    lo, hi = min(x for iv in intervals for x in iv), max(x for iv in intervals for x in iv)
    return [(lo, hi)]


def _wraps_seam(intervals: list[tuple[float, float]]) -> bool:
    return any(a > b for a, b in intervals)
