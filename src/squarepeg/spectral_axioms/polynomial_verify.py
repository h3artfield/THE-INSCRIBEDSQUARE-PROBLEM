"""Polynomial and integral countermodel candidates."""

from __future__ import annotations

from fractions import Fraction
from typing import Callable

from squarepeg.spectral_axioms.continuum_cells import PLFunction, certify_pl_subadditivity


def integral_countermodel_w(
    epsilon: float = 0.01,
    p: float = 2.0,
    samples: int = 400,
) -> dict:
    """
    g(x) = ∫_0^x w(t) dt / ∫_0^1 w(t) dt with w(t) = (t-0.5)^2 + epsilon.
    Strictly increasing, w(0.5)>0 so g'(0.5)>0 — NOT a D+=0 candidate.
    """
    import math

    def w(t: float) -> float:
        return (t - 0.5) ** p + epsilon

    dt = 1.0 / samples
    ws = [w(i * dt) for i in range(samples + 1)]
    total = sum((ws[i] + ws[i + 1]) / 2 * dt for i in range(samples))

    def g(x: float) -> float:
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        n = int(x * samples)
        partial = sum((ws[i] + ws[i + 1]) / 2 * dt for i in range(n))
        partial += (w(n * dt) + w(x)) / 2 * (x - n * dt)
        return partial / total

    return {"name": "integral_w", "g": g, "D_plus_positive": True}


def weak_pl_flat_midpoint(kappa: float, flat_half_width: float = 0.0125) -> PLFunction:
    """
    Model W: flat at midpoint, linear rise elsewhere.
    g=0 on [0, 0.5-h0], flat on [0.5-h0, 0.5+h0], linear to 1 on [0.5+h0, 1].
    """
    h0 = Fraction(flat_half_width).limit_denominator(10000)
    half = Fraction(1, 2)
    v_flat = Fraction(0)  # value on flat region (connected to 0 on left)
    x_r = half + h0
    slope_r = (Fraction(1) - v_flat) / (Fraction(1) - x_r)
    if float(slope_r) > kappa + 1e-9:
        raise ValueError(f"slope {slope_r} exceeds kappa {kappa}")
    bps = [
        (Fraction(0), Fraction(0)),
        (half - h0, Fraction(0)),
        (half + h0, Fraction(0)),
        (Fraction(1), Fraction(1)),
    ]
    return PLFunction(bps)


def search_strict_C2_countermodel(kappa: float) -> dict:
    """
    Attempt g(x) = x + a*(x-1/2)^3 for small a (strict, g'(1/2)=1).
    D+(g,1/2) = 1 always. Cannot achieve D+=0.
    """
    return {
        "name": "cubic_perturbation",
        "D_plus": 1.0,
        "strict": True,
        "viable_for_D_plus_zero": False,
        "reason": "g'(1/2)=1 from analytic expansion",
    }


def accumulating_breakpoints_model(n_terms: int = 20) -> dict:
    """
    Infinite-breakpoint limit: breakpoints at 1/2 ± 2^{-k}.
    NOT implemented as finite strict PL with D+=0 per obstruction lemma.
    """
    return {
        "name": "accumulating_breakpoints",
        "status": "UNRESOLVED",
        "note": "Requires limit analysis; finite truncations are strict PL with D+>0",
    }
