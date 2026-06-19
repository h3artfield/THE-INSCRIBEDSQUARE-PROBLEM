"""Cross-scale and scale-escape search (T036-N2/N3 diagnostic)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ScaleEscape = Literal["FIXED_SCALE_LIMSUP", "SHRINKING_PACKETS", "UNRESOLVED"]


@dataclass
class PacketTreeNode:
    packet_id: str
    center: tuple[float, float]
    scale: float
    sign: int
    depth: int
    robustness_radius: float
    parent_id: str | None
    children: list[str] = field(default_factory=list)


@dataclass
class CrossScaleSearchReport:
    escape_classification: ScaleEscape
    fixed_scale_component: bool
    cross_scale_candidate: bool
    notes: list[str]


def classify_scale_escape(scales: list[float]) -> ScaleEscape:
    if not scales:
        return "UNRESOLVED"
    tail = scales[-5:] if len(scales) >= 5 else scales
    limsup = max(tail)
    if limsup > 0.05:
        return "FIXED_SCALE_LIMSUP"
    if max(scales) < 0.05 and min(scales) < 0.01 and len(scales) > 3:
        return "SHRINKING_PACKETS"
    return "UNRESOLVED"


def search_cross_scale(nodes: list[PacketTreeNode]) -> CrossScaleSearchReport:
    scales = [n.scale for n in nodes]
    esc = classify_scale_escape(scales)
    cross = any(
        n.parent_id is not None and n.robustness_radius > 0.01 for n in nodes
    )
    return CrossScaleSearchReport(
        escape_classification=esc,
        fixed_scale_component=esc == "FIXED_SCALE_LIMSUP",
        cross_scale_candidate=cross,
        notes=[
            "T036-N2: fixed limsup => limiting protected square via T031/T039",
            "Shrinking packets => local packet-scale squares only (T036-N1 local conclusion)",
            "T036-N3 cross-scale component: actively seek counterexamples",
        ],
    )


def t036_n2_statement() -> str:
    return (
        "T036-N2 (CONJECTURAL_SELECTION_TARGET): Either outer packet scales have positive "
        "limsup (fixed-scale protected component) or scales -> 0 (confined defect; not area-tight)."
    )


def t036_n3_statement() -> str:
    return (
        "T036-N3 (CONJECTURAL_CROSS_SCALE_TARGET): Infinite nested chain may create cross-scale "
        "cyclic-odd component at largest persistent scale — not assumed; seek counterexamples."
    )
