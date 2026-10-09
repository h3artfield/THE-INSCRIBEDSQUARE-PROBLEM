"""Curve-level parameter support geometry (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

SupportClass = Literal[
    "CONNECTED",
    "FINITE_DISCONNECTED",
    "COUNTABLE_DISCONNECTED",
    "CANTOR_DISCONNECTED",
    "DUST_LIKE",
    "HARMLESS_QUOTIENT",
]


@dataclass
class ParameterSupportRecord:
    support_id: str
    component_count: int
    support_class: SupportClass
    gap_mass: float
    curve_level: bool


@dataclass
class ParameterSupportAudit:
    records: list[ParameterSupportRecord]
    curve_level: bool
    connected: bool
    messages: list[str]


def _leaf_intervals(tree: CanonicalIntrusionTree) -> list[tuple[float, float]]:
    leaves = [n for n in tree.nodes.values() if not n.child_ids]
    return sorted((n.param_interval for n in leaves), key=lambda x: x[0])


def _gap_mass(intervals: list[tuple[float, float]]) -> float:
    if len(intervals) < 2:
        return 0.0
    gaps = 0.0
    for i in range(len(intervals) - 1):
        g = intervals[i + 1][0] - intervals[i][1]
        if g > 1e-9:
            gaps += g
    return gaps


def _classify_support(intervals: list[tuple[float, float]], gap: float) -> SupportClass:
    if gap < 1e-9 and len(intervals) <= 1:
        return "CONNECTED"
    if gap < 1e-9:
        return "CONNECTED"
    n = len(intervals)
    if n <= 4 and gap > 0:
        return "FINITE_DISCONNECTED"
    if n <= 32:
        return "COUNTABLE_DISCONNECTED"
    widths = [hi - lo for lo, hi in intervals]
    if max(widths) < 0.01 and n > 8:
        return "DUST_LIKE"
    return "CANTOR_DISCONNECTED"


def audit_parameter_support(tree: CanonicalIntrusionTree) -> ParameterSupportAudit:
    intervals = _leaf_intervals(tree)
    gap = _gap_mass(intervals)
    sc = _classify_support(intervals, gap)
    if gap < 1e-9 and len(intervals) > 1:
        sc = "HARMLESS_QUOTIENT" if all(hi - lo > 0 for lo, hi in intervals) else "CONNECTED"
    records = [
        ParameterSupportRecord(
            "primary",
            max(len(intervals), 1),
            sc,
            gap,
            True,
        )
    ]
    connected = sc in ("CONNECTED", "HARMLESS_QUOTIENT")
    return ParameterSupportAudit(records, True, connected, [f"class={sc}, gap={gap:.6f}"])
