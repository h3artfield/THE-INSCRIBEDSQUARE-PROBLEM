"""Young integrals and Liouville primitive estimates (AI-PEG-v3 convention)."""

from __future__ import annotations

import math
from fractions import Fraction

from squarepeg.variation.p_variation import FracPoint, Point, p_variation

PointF = Point


def zeta_s(s: float) -> float:
    """Riemann zeta; only s>1 used here."""
    if s <= 1.0:
        raise ValueError("zeta requires s > 1")
    # Direct partial sum for small s used in Young estimates.
    n = 100000
    return sum(1.0 / k**s for k in range(1, n + 1))


def young_pairing_bound(q: float) -> float:
    """
    Constant 2*zeta(2/q) from BG Theorem 3.1 / AI convergence template (q<2).
    """
    if q <= 0 or q >= 2:
        raise ValueError("require 0 < q < 2")
    return 2.0 * zeta_s(2.0 / q)


def liouville_integrand_xi_dx(p0: FracPoint, p1: FracPoint) -> Fraction:
    """
    ∫ ξ dx on segment with linear (x,ξ); λ = ξ dx (AI-PEG-v3).
    """
    x0, xi0 = p0
    x1, xi1 = p1
    return (xi0 + xi1) * (x1 - x0) / 2


def primitive_from_points_frac(
    points: list[FracPoint],
    base: Fraction = Fraction(0),
) -> list[Fraction]:
    if not points:
        return []
    vals = [base]
    acc = base
    for i in range(len(points) - 1):
        acc += liouville_integrand_xi_dx(points[i], points[i + 1])
        vals.append(acc)
    return vals


def primitive_from_points(
    points: list[PointF],
    base: float = 0.0,
) -> list[float]:
    """Trapezoid rule along PL path (exact when coordinates linear on segments)."""
    if not points:
        return []
    vals = [base]
    acc = base
    for i in range(len(points) - 1):
        x0, xi0 = points[i]
        x1, xi1 = points[i + 1]
        acc += 0.5 * (xi0 + xi1) * (x1 - x0)
        vals.append(acc)
    return vals


def closed_liouville_integral(points: list[PointF]) -> float:
    """One-period ∮ ξ dx (signed area term in AI convention)."""
    if len(points) < 2:
        return 0.0
    return primitive_from_points(points)[-1] - primitive_from_points(points)[0]


def classical_area_from_points_frac(points: list[FracPoint]) -> Fraction:
    n = len(points)
    if n < 3:
        return Fraction(0)
    twice = Fraction(0)
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        twice += x0 * y1 - x1 * y0
    return abs(twice) / 2


def classical_area_from_points(points: list[PointF]) -> float:
    n = len(points)
    if n < 3:
        return 0.0
    twice = 0.0
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        twice += x0 * y1 - x1 * y0
    return abs(twice) / 2


def young_primitive_increment_bound(
    q: float,
    diff_qvar: float,
    path_qvar: float,
    integrand_qvar: float,
    integrand_diff_qvar: float,
) -> float:
    """
    Bound |∫(ξ_n-ξ)dx_n| + |∫ξ d(x_n-x)| using BG Thm 3.1 template.

    Returns uniform-in-interval increment bound on one period.
    """
    c = young_pairing_bound(q)
    return c * (
        integrand_diff_qvar * path_qvar + integrand_qvar * diff_qvar
    )


def max_primitive_gap(prim_a: list[float], prim_b: list[float]) -> float:
    if len(prim_a) != len(prim_b):
        raise ValueError("common partition required")
    return max(abs(a - b) for a, b in zip(prim_a, prim_b))


def lift_periodic_primitive(values_on_period: list[float], periods: int) -> list[float]:
    """Extend f(t+2π) = f(t) + I for |t| <= periods * 2π sample."""
    if not values_on_period:
        return []
    period_integral = values_on_period[-1] - values_on_period[0]
    out: list[float] = []
    for k in range(periods):
        shift = k * period_integral
        out.extend(v + shift for v in values_on_period[:-1])
    out.append(values_on_period[-1] + (periods - 1) * period_integral)
    return out


def coords_from_points(points: list[PointF]) -> tuple[list[float], list[float]]:
    xs = [p[0] for p in points]
    xis = [p[1] for p in points]
    return xs, xis


def p_variation_coord(values: list[float], p: float) -> float:
    pts = [(v, 0.0) for v in values]
    return p_variation(pts, p)
