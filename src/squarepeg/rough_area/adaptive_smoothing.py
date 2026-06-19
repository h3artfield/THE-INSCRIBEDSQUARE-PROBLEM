"""Adaptive T018 smoothing with primitive control (Directive 008R)."""

from __future__ import annotations

import math

from squarepeg.rough_area.liouville_recovery import recover_primitive
from squarepeg.variation.cubic_corner_smoothing import _resample_polyline
from squarepeg.variation.p_variation import path_difference, p_variation, total_variation
from squarepeg.variation.smoothing import SmoothedPolygon, round_corners_c1
from squarepeg.variation.young_integral import max_primitive_gap, primitive_from_points

Point = tuple[float, float]


def coordinate_sup_norm(points: list[Point]) -> float:
    if not points:
        return 0.0
    return max(max(abs(p[0]), abs(p[1])) for p in points)


def polygon_variation_1(points: list[Point]) -> float:
    return total_variation(points)


def choose_smoothing_tolerance(
    ln: float,
    mn: float,
    target: float,
) -> float:
    """
    Choose epsilon_n > 0 with epsilon_n (L_n + M_n + epsilon_n) < target.

    Returns epsilon_n -> 0 as target -> 0 even when L_n grows.
    """
    if ln + mn <= 0:
        return min(target, 1e-3)
    disc = (ln + mn) ** 2 + 4.0 * target
    eps = (-(ln + mn) + math.sqrt(disc)) / 2.0
    # Slight shrinkage for strict inequality under floating-point arithmetic.
    return max(eps * 0.999, 1e-12)


def smoothing_primitive_bound(epsilon: float, ln: float, mn: float) -> float:
    """Directive 008R §12: sup_t |f^S - f^P| <= epsilon (L + M + epsilon)."""
    return epsilon * (ln + mn + epsilon)


def adaptive_smooth_polygon(
    polygon: list[Point],
    n_resample: int = 64,
    target_error: float = 1e-3,
) -> tuple[SmoothedPolygon, float, float]:
    """
    Apply T018 with tolerance derived from L_n, M_n.

    Returns (SmoothedPolygon, epsilon_n, predicted_primitive_bound).
    """
    ln = polygon_variation_1(polygon)
    mn = coordinate_sup_norm(polygon) + 1.0
    eps = choose_smoothing_tolerance(ln, mn, target_error)
    sm = round_corners_c1(polygon, epsilon=eps)
    return sm, eps, smoothing_primitive_bound(eps, ln, mn)


def verify_smoothing_primitive_control(
    polygon: list[Point],
    sm: SmoothedPolygon,
    epsilon: float,
) -> tuple[float, float]:
    """
    Verify sup |f^S - f^P| <= epsilon (L+M+eps) on resampled common grid.
    """
    n = min(len(polygon), len(sm.smoothed), 64)
    p = _resample_polyline(polygon, n)
    s = _resample_polyline(sm.smoothed, n)
    fp = primitive_from_points(p)
    fs = primitive_from_points(s)
    gap = max_primitive_gap(fp, fs)
    ln = polygon_variation_1(polygon)
    mn = coordinate_sup_norm(polygon) + 1.0
    bound = smoothing_primitive_bound(epsilon, ln, mn)
    return gap, bound


def lifted_primitive_bound(
    eta_n: float,
    period_gap: float,
    k: int,
) -> float:
    """sup_{|t|<=K} |f_n - f| <= eta_n + (ceil(K)+1)|I_n - I| with K ~ k."""
    return eta_n + (abs(k) + 1) * abs(period_gap)
