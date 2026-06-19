"""Bounded-gate join estimates J_M(r) (Directive 030)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_surgery.concatenation_area import wedge

Point = tuple[float, float]

C_COLLAR = 1.0


@dataclass
class JoinBoundAudit:
    gate_bound_m: int
    component_count_q: int
    join_upper_bound: float
    diameter_r: float
    increment_bound: float
    formula: str


def q_of_m(m: int) -> int:
    """
    Explicit component-count bound Q(M) for M-gate outerplanar cluster.

    Uses: edges <= 2M-3, blocks <= M, filler <= M => Q(M) <= 3M.
    """
    return max(3 * m, 4)


def j_m_r(m: int, r: float, *, c_collar: float = C_COLLAR) -> float:
    """J_M(r) = (1/2) binom(Q(M),2) C_collar^2 r^2."""
    q = q_of_m(m)
    return 0.5 * q * (q - 1) * c_collar ** 2 * r ** 2


def increment_bound(diameter_r: float, *, c_collar: float = C_COLLAR) -> float:
    """|Delta_i| <= C_collar * r(C) for endpoints in H(C)."""
    return c_collar * diameter_r


def audit_join_bound(*, m: int, diameter_r: float) -> JoinBoundAudit:
    """Verify analytic join bound independent of internal winding."""
    q = q_of_m(m)
    j = j_m_r(m, diameter_r)
    return JoinBoundAudit(
        gate_bound_m=m,
        component_count_q=q,
        join_upper_bound=j,
        diameter_r=diameter_r,
        increment_bound=increment_bound(diameter_r),
        formula=f"J_{m}(r) = 0.5*binom({q},2)*{C_COLLAR}^2*r^2",
    )


def join_from_components(
    increments: list[Point],
    *,
    m: int,
    diameter_r: float,
) -> tuple[float, float]:
    """
    Compute exact pairwise join and compare to J_M(r) upper bound.

    Returns (exact_join, upper_bound).
    """
    exact = 0.0
    for i in range(len(increments)):
        for j in range(i + 1, len(increments)):
            exact += 0.5 * wedge(increments[i], increments[j])
    return exact, j_m_r(m, diameter_r)


def join_bound_holds(exact_join: float, m: int, diameter_r: float, tol: float = 1e-9) -> bool:
    return abs(exact_join) <= j_m_r(m, diameter_r) + tol
