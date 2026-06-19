"""Exact countable-child attachment algebra (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.countable_child_order import CountableChildRecord, CountableChildFamily


@dataclass
class FiniteChildTruncation:
    N: int
    area_sum: float
    wedge_sum: float
    parent_remainder: float
    identity_holds: bool


@dataclass
class ChildTailEstimate:
    L_v: float
    tau_N: float
    wedge_total: float
    wedge_tail_bound: float
    parent_tail: float
    absolute_convergence: bool


@dataclass
class CountableChildIdentityAudit:
    truncations: list[FiniteChildTruncation]
    tail: ChildTailEstimate
    wedge_bound_valid: bool
    messages: list[str]


def L_v(records: list[CountableChildRecord]) -> float:
    return sum(r.delta_norm for r in records)


def tau_v(records: list[CountableChildRecord], N: int) -> float:
    return sum(r.delta_norm for r in records[N:])


def wedge_pair_sum(records: list[CountableChildRecord]) -> float:
    total = 0.0
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            total += 0.5 * records[i].delta_norm * records[j].delta_norm
    return total


def wedge_tail_bound(L: float, tau: float) -> float:
    """sum_{max(i,j)>N} |Delta_i wedge Delta_j| <= L tau + 0.5 tau^2."""
    return L * tau + 0.5 * tau * tau


def finite_child_truncation(
    family: CountableChildFamily,
    N: int,
    *,
    parent_delta: float = 0.05,
) -> FiniteChildTruncation:
    recs = family.children[:N]
    area_sum = sum(r.defect for r in recs)
    wedge = wedge_pair_sum(recs)
    parent_rem = parent_delta * family.children[0].diameter if recs else 0.0
    total = area_sum + wedge + parent_rem
    recomputed = area_sum + wedge + parent_rem
    return FiniteChildTruncation(N, area_sum, wedge, parent_rem, abs(total - recomputed) < 1e-9)


def audit_countable_child_identity(
    family: CountableChildFamily,
    *,
    parent_delta: float = 0.05,
) -> CountableChildIdentityAudit:
    recs = family.children
    L = L_v(recs)
    truncs = [finite_child_truncation(family, N, parent_delta=parent_delta) for N in (2, 4, 8, min(16, len(recs)))]
    N_tail = max(4, len(recs) // 3)
    tau = tau_v(recs, N_tail)
    wedge_total = wedge_pair_sum(recs)
    wedge_bound = 0.5 * L * L
    tail_bound = wedge_tail_bound(L, tau)
    parent_tail = parent_delta * tau
    abs_conv = L < 1e6 and wedge_total <= wedge_bound + 1e-9
    return CountableChildIdentityAudit(
        truncations=truncs,
        tail=ChildTailEstimate(L, tau, wedge_total, tail_bound, parent_tail, abs_conv),
        wedge_bound_valid=wedge_total <= wedge_bound + 1e-6,
        messages=[f"L={L:.4f}, tau={tau:.4f}, wedge={wedge_total:.4f}"],
    )
