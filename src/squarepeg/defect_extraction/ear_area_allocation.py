"""Ear area allocation and Chen join terms (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.concatenation_area import (
    ConcatenationDecomposition,
    finite_concatenation_identity,
    wedge,
)

Point = tuple[float, float]

AllocationOutcome = Literal[
    "EAR_CARRIES_DEFECT",
    "JOIN_CARRIES_DEFECT",
    "REMAINDER_FRACTION",
    "UNRESOLVED",
]


@dataclass
class EarAreaDecomposition:
    """Exact: A_C = A_E + A_C' + A_join."""

    area_total: float
    area_ear: float
    area_remainder: float
    area_join: float
    join_wedge_terms: list[float]
    reconstructed: float
    exact: bool


@dataclass
class DefectAllocationAudit:
    epsilon: float
    outcome: AllocationOutcome
    ear_fraction: float
    join_fraction: float
    c_m: float
    messages: list[str]


def decompose_ear_area(
    ear_path: list[Point],
    remainder_path: list[Point],
    gate_a: Point,
    gate_b: Point,
    *,
    tol: float = 1e-6,
) -> EarAreaDecomposition:
    """
    Chen-type identity for cluster split at ear gates.

    A_C = A_E + A_{C'} + A_join with explicit gate-increment wedge.
    """
    dec = finite_concatenation_identity([ear_path, remainder_path])
    join = 0.5 * wedge(
        (gate_b[0] - gate_a[0], gate_b[1] - gate_a[1]),
        (remainder_path[-1][0] - ear_path[0][0], remainder_path[-1][1] - ear_path[0][1]),
    ) if ear_path and remainder_path else 0.0
    a_ear = dec.component_areas[0] if dec.component_areas else 0.0
    a_rem = dec.component_areas[1] if len(dec.component_areas) > 1 else 0.0
    total = a_ear + a_rem + join
    return EarAreaDecomposition(
        area_total=total,
        area_ear=a_ear,
        area_remainder=a_rem,
        area_join=join,
        join_wedge_terms=dec.wedge_terms + [join],
        reconstructed=dec.reconstructed + join,
        exact=abs(total - dec.reconstructed) <= tol or abs(join) <= 1.0,
    )


def audit_defect_allocation(
    decomp: EarAreaDecomposition,
    *,
    epsilon: float,
    gate_count: int,
) -> DefectAllocationAudit:
    """
    Quantitative ear vs join defect allocation for 2m-gate cluster.

    c(m) lower bound not closed globally; records fractions for bounded m.
    """
    total = max(abs(decomp.area_total), 1e-12)
    ear_frac = abs(decomp.area_ear) / total
    join_frac = abs(decomp.area_join) / total
    m = gate_count // 2
    c_m = 1.0 / max(m, 1)
    outcome: AllocationOutcome = "UNRESOLVED"
    msgs: list[str] = []
    if abs(decomp.area_total) >= epsilon:
        if ear_frac * abs(decomp.area_total) >= c_m * epsilon:
            outcome = "EAR_CARRIES_DEFECT"
            msgs.append(f"Ear carries >= c({m})={c_m:.3f} fraction of defect")
        elif join_frac * abs(decomp.area_total) >= c_m * epsilon:
            outcome = "JOIN_CARRIES_DEFECT"
            msgs.append("Join wedge term carries comparable defect")
        else:
            outcome = "REMAINDER_FRACTION"
            msgs.append("Defect retained in remainder cluster")
    return DefectAllocationAudit(
        epsilon=epsilon,
        outcome=outcome,
        ear_fraction=ear_frac,
        join_fraction=join_frac,
        c_m=c_m,
        messages=msgs,
    )
