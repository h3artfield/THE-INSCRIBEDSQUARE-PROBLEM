"""Genuine smooth truncations (Directive 012 fallback)."""

from __future__ import annotations

import math

from squarepeg.residual_curves.canonical import CANONICAL_THETA0, CANONICAL_EPS_FLOAT
from squarepeg.residual_curves.double_spiral import gamma_minus, gamma_plus


def smooth_tail_cutoff(theta: float, theta_cut: float) -> float:
    """C^1 bump: 1 for theta<=cut, 0 for theta large."""
    if theta <= theta_cut:
        return 1.0
    if theta >= theta_cut + 1.0:
        return 0.0
    t = (theta - theta_cut)
    return 0.5 * (1.0 + math.cos(math.pi * t))


def smooth_truncation_outer(theta: float, theta_cut: float) -> tuple[float, float]:
    """Outer arm point with inner tail replaced by origin approach."""
    w = smooth_tail_cutoff(theta, theta_cut)
    if w <= 0:
        return (0.0, 0.0)
    x, y = gamma_plus(theta)
    return w * x, w * y
