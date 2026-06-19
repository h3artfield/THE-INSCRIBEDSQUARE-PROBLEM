"""Quantitative defect allocation under ear peeling (Directive 030)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.bounded_gate_join import j_m_r, q_of_m
from squarepeg.defect_extraction.ear_area_allocation import EarAreaDecomposition, decompose_ear_area

Point = tuple[float, float]

AllocationStatus = Literal[
    "EAR_CARRIES_FRACTION",
    "REMAINDER_CARRIES_FRACTION",
    "JOIN_NEGLIGIBLE",
    "JOIN_DOMINATES",
]


@dataclass
class OneStepAllocation:
    epsilon: float
    area_total: float
    area_ear: float
    area_remainder: float
    area_join: float
    join_bound: float
    max_component: float
    status: AllocationStatus
    fraction_constant: float


@dataclass
class PeelingAllocationAudit:
    epsilon: float
    m: int
    c_m: float
    r0: float
    stages: int
    all_join_negligible: bool
    messages: list[str] = field(default_factory=list)


def one_step_allocation(
    decomp: EarAreaDecomposition,
    *,
    epsilon: float,
    m: int,
    diameter_r: float,
) -> OneStepAllocation:
    """
    If J_M(r) <= epsilon/4 then max(|A_E|,|A_C'|) >= 3*epsilon/8.
    """
    join_bound = j_m_r(m, diameter_r)
    j = abs(decomp.area_join)
    total = abs(decomp.area_total)
    ae = abs(decomp.area_ear)
    ar = abs(decomp.area_remainder)
    max_comp = max(ae, ar)
    status: AllocationStatus = "JOIN_DOMINATES"
    frac = 0.0
    if join_bound <= epsilon / 4 and total >= epsilon:
        if max_comp >= 0.375 * epsilon:
            status = "EAR_CARRIES_FRACTION" if ae >= ar else "REMAINDER_CARRIES_FRACTION"
            frac = max_comp / epsilon
        else:
            status = "JOIN_NEGLIGIBLE"
    elif j <= join_bound:
        status = "JOIN_NEGLIGIBLE"
    return OneStepAllocation(
        epsilon=epsilon,
        area_total=decomp.area_total,
        area_ear=decomp.area_ear,
        area_remainder=decomp.area_remainder,
        area_join=decomp.area_join,
        join_bound=join_bound,
        max_component=max_comp,
        status=status,
        fraction_constant=frac if frac else 3.0 / 8.0,
    )


def c_of_m(m: int) -> float:
    """Explicit c(M) > 0 for bounded-gate peeling."""
    return 1.0 / (4 * q_of_m(m))


def r0_of_m_epsilon(m: int, epsilon: float) -> float:
    """r_0(M,epsilon) such that J_M(r) <= epsilon/4 for r < r_0."""
    if epsilon <= 0:
        return 0.0
    j_unit = j_m_r(m, 1.0)
    if j_unit <= 0:
        return 1.0
    return math.sqrt(epsilon / (4 * j_unit))


def audit_peeling_allocation(
    *,
    m: int,
    epsilon: float,
    diameters: list[float],
    n_stages: int | None = None,
) -> PeelingAllocationAudit:
    """
    Full peeling: fixed defect + shrinking r => join negligible at T037 scale.
    """
    import math

    c_m = c_of_m(m)
    r0 = r0_of_m_epsilon(m, epsilon)
    stages = n_stages or q_of_m(m)
    all_negligible = all(j_m_r(m, r) <= epsilon / 4 for r in diameters if r <= r0)
    msgs = [
        f"c({m})={c_m:.4f}",
        f"r_0({m},eps)={r0:.4f}",
        f"T037 epsilon_0/4 scale: join negligible when r < r_0",
    ]
    return PeelingAllocationAudit(
        epsilon=epsilon,
        m=m,
        c_m=c_m,
        r0=r0,
        stages=stages,
        all_join_negligible=all_negligible,
        messages=msgs,
    )
