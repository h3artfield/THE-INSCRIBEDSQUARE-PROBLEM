"""Recursive gate concentration (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DescentClass = Literal[
    "INFINITE_INTRUSION_RAY",
    "ANNULAR_TOWER",
    "MULTICENTER_ALTERNATING",
    "DENSE_GATE_CANTOR",
    "TERMINATED",
]


@dataclass
class ConcentratedSubblock:
    block_id: str
    gate_ids: list[str]
    attachment_area: float
    diameter: float
    defect_fraction: float


@dataclass
class ConcentrationAudit:
    subblock: ConcentratedSubblock | None
    scale_ratio: float
    descent_class: DescentClass
    nested_scales: list[float]
    messages: list[str]


def extract_concentrated_subblock(
    gate_ids: list[str],
    spacings: list[float],
    attachment_areas: list[float],
    *,
    r: float,
    epsilon: float = 0.025,
    c: float = 0.25,
) -> ConcentrationAudit:
    """
    D2: consecutive block B_n with |A_{Z(B_n)}| >= c*epsilon and diam = o(r).
    """
    if not gate_ids or not attachment_areas:
        return ConcentrationAudit(None, 0.0, "TERMINATED", [], ["No gates"])
    best_idx = 0
    best_mass = 0.0
    window = min(4, len(gate_ids))
    for i in range(len(gate_ids) - window + 1):
        chunk = attachment_areas[i : i + window]
        mass = abs(sum(chunk))
        if mass > best_mass:
            best_mass = mass
            best_idx = i
    chunk_ids = gate_ids[best_idx : best_idx + window]
    chunk_diam = sum(spacings[best_idx : best_idx + window]) * r if spacings else r
    frac = best_mass / epsilon if epsilon > 0 else 0.0
    sub = None
    descent: DescentClass = "TERMINATED"
    scales = [r]
    if frac >= c and chunk_diam < r:
        sub = ConcentratedSubblock(
            block_id=f"conc_{best_idx}",
            gate_ids=chunk_ids,
            attachment_area=best_mass,
            diameter=chunk_diam,
            defect_fraction=frac,
        )
        descent = "INFINITE_INTRUSION_RAY" if chunk_diam < r / 4 else "ANNULAR_TOWER"
        scales = [r, chunk_diam, chunk_diam / 2]
    return ConcentrationAudit(
        subblock=sub,
        scale_ratio=chunk_diam / r if r > 0 else 0.0,
        descent_class=descent,
        nested_scales=scales,
        messages=[f"Concentration fraction={frac:.3f}"],
    )
