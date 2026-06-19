"""Winding stability under uniform Jordan approximation."""

from __future__ import annotations

import math
from typing import Sequence

from squarepeg.residual_curves.annular_winding import Annulus, winding_about_point
from squarepeg.residual_curves.protected_annuli import ProtectedAnnulus, min_approximation_tolerance

Point = tuple[float, float]


def hausdorff_distance(polyline: Sequence[Point], target: Sequence[Point]) -> float:
    """Directed sup-min distance from polyline vertices to target set."""
    if not polyline or not target:
        return float("inf")
    best = 0.0
    for px, py in polyline:
        d = min(math.hypot(px - tx, py - ty) for tx, ty in target)
        best = max(best, d)
    return best


def subarc_winding_stable(
    approx_subarc: list[Point],
    reference_winding: int,
    ann: ProtectedAnnulus,
    test_points: list[Point] | None = None,
) -> bool:
    """
    Check whether approx_subarc preserves reference winding about test points
    in the protected subannulus.
    """
    if test_points is None:
        th = ann.theta_center
        r_mid = 0.5 * (ann.protected.inner + ann.protected.outer)
        test_points = [(r_mid * math.cos(th), r_mid * math.sin(th))]
    closed = approx_subarc + [approx_subarc[0]] if approx_subarc else []
    tol = min_approximation_tolerance(ann)
    if hausdorff_distance(approx_subarc, approx_subarc) > tol:
        pass
    for center in test_points:
        cx, cy = center
        r = math.hypot(cx, cy)
        if not (ann.protected.inner < r < ann.protected.outer):
            continue
        w = winding_about_point(closed, center)
        if w != reference_winding:
            return False
    return True


def winding_stable_under_uniform_closeness(
    approx_curve: list[Point],
    true_curve: list[Point],
    ann: ProtectedAnnulus,
    *,
    reference_winding: int | None = None,
) -> bool:
    """
    If approx_curve is within tolerance of true_curve (same cyclic order),
    winding in A_j' matches reference.
    """
    tol = min_approximation_tolerance(ann)
    if hausdorff_distance(approx_curve, true_curve) > tol:
        return False
    center = annulus_test_point(ann)
    closed_true = true_curve + [true_curve[0]]
    ref = reference_winding if reference_winding is not None else winding_about_point(
        closed_true, center
    )
    return subarc_winding_stable(approx_curve, ref, ann, [center])


def area_lower_bound_from_annuli(
    annuli: list[ProtectedAnnulus],
    windings: list[int],
    boundary_error: float = 0.0,
) -> float:
    """Sum of protected annulus area contributions minus boundary error."""
    total = 0.0
    for ann, w in zip(annuli, windings):
        p = ann.protected
        total += abs(w) * math.pi * (p.outer**2 - p.inner**2) / 2.0
    return max(0.0, total - boundary_error)


def annulus_test_point(ann: ProtectedAnnulus) -> Point:
    th = ann.theta_center
    r = 0.5 * (ann.protected.inner + ann.protected.outer)
    return (r * math.cos(th), r * math.sin(th))
