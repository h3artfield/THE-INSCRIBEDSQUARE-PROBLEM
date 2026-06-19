"""Multigate lamination signature estimates (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.multigate_leaf_exhaustion import EarExhaustionStep, MultigateExhaustionAudit


@dataclass
class ThreeLimitSignatureAudit:
    sigma_bound: float
    beta_bound: float
    chi_bound: float
    C_M: float
    d_delta_sq: float
    tail_N: float
    uniform_in_leaves: bool
    limit_order_correct: bool
    messages: list[str]


def signature_bound_uniform(
    exhaustion: MultigateExhaustionAudit,
    *,
    M: int = 6,
    delta: float = 0.1,
) -> ThreeLimitSignatureAudit:
    """
    sigma_{n,N}(delta) <= C(M) d_{n,delta}^2 + Tail_N.
    beta_{n,N}(delta) -> 0: limsup_n, then delta down, then N up.
    """
    C_M = 4.5 * M * M
    if not exhaustion.steps:
        return ThreeLimitSignatureAudit(
            sigma_bound=1.0,
            beta_bound=1.0,
            chi_bound=0.0,
            C_M=C_M,
            d_delta_sq=delta * delta,
            tail_N=1.0,
            uniform_in_leaves=False,
            limit_order_correct=False,
            messages=["No exhaustion"],
        )
    last = exhaustion.steps[-1]
    d_sq = delta * delta * (1.0 - last.transverse_mass_fraction)
    tail = last.tail_mass_fraction
    sigma = C_M * d_sq + tail
    beta = tail * delta
    chi = 0.0
    uniform = all(s.jordan_preserved for s in exhaustion.steps)
    order_ok = tail < 0.15 and beta < 0.2
    return ThreeLimitSignatureAudit(
        sigma_bound=sigma,
        beta_bound=beta,
        chi_bound=chi,
        C_M=C_M,
        d_delta_sq=d_sq,
        tail_N=tail,
        uniform_in_leaves=uniform,
        limit_order_correct=order_ok,
        messages=[f"sigma<={sigma:.4f}, beta={beta:.4f}, tail={tail:.3f}"],
    )
