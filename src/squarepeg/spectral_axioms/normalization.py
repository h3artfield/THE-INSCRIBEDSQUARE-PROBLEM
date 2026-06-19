"""Normalized spectral functions g(x) = ℓ(πx)/A."""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

Number = Fraction | int | float


def B_from_area_radius(area: Number, radius: Number) -> Fraction:
    a, r = Fraction(area), Fraction(radius)
    if r <= 0:
        raise ValueError("radius must be positive")
    return a / (r * r)


def kappa_from_B(B: Number) -> Fraction:
    """κ = π R² / A = π / B with rational π approximation."""
    return _pi_rational() / Fraction(B)


def kappa_from_area_radius(area: Number, radius: Number) -> Fraction:
    return kappa_from_B(B_from_area_radius(area, radius))


def _pi_rational() -> Fraction:
    from math import pi

    return Fraction(pi).limit_denominator(10**12)


def normalize_spectral(ell_theta: Number, area: Number) -> Fraction:
    return Fraction(ell_theta) / Fraction(area)


def midpoint_quotient(g_at_lo: Number, g_at_hi: Number, h: Number) -> Fraction:
    """D_h(g) = (g(1/2+h)-g(1/2-h))/(2h); pass values at lo/hi symmetric points."""
    return (Fraction(g_at_hi) - Fraction(g_at_lo)) / (2 * Fraction(h))


def D_plus_at_half(values: Sequence[Number], xs: Sequence[Number]) -> Fraction:
    """Grid estimate of limsup symmetric midpoint quotient."""
    best = Fraction(0)
    half = Fraction(1, 2)
    for i, x in enumerate(xs):
        xf = Fraction(x)
        if xf <= half:
            continue
        h = xf - half
        partner = half - h
        j = min(range(len(xs)), key=lambda k: abs(Fraction(xs[k]) - partner))
        q = midpoint_quotient(values[j], values[i], h)
        if q > best:
            best = q
    return best
