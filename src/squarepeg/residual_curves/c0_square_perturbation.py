"""C^0 perturbation bounds and robust square existence (T027)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from squarepeg.residual_curves.iv_backend_v1 import (
    boxes_from_fractions,
    gamma_plus_interval,
    min_radius_lower_bound,
    pairwise_separation_lower_bounds,
    side_length_lower_bound,
)
from squarepeg.residual_curves.t025_frozen_constants import KRAWCZYK_THETA_BOXES, SUPPORT_THETA_INTERVALS


def R_max_on_support_boxes() -> float:
    """R = max_i max_{u in J_i} |p_i(u)| over certified support windows."""
    boxes = tuple((float(lo), float(hi)) for lo, hi in SUPPORT_THETA_INTERVALS)
    ivs = boxes_from_fractions(boxes)
    m = 0.0
    for iv in ivs:
        x, y = gamma_plus_interval(iv)
        for vx in (x.lo, x.hi):
            for vy in (y.lo, y.hi):
                m = max(m, math.hypot(vx, vy))
    return m


def squared_distance_perturbation_bound(eta: float, R: float | None = None) -> float:
    """
    | |a'-b'|^2 - |a-b|^2 | <= 8 R eta + 4 eta^2
    for |a'-a|, |b'-b| <= eta and |a|,|b| <= R.
    """
    if R is None:
        R = R_max_on_support_boxes()
    return 8.0 * R * eta + 4.0 * eta * eta


def F_perturbation_bound(eta: float, R: float | None = None) -> float:
    """
    Each component of F is a difference of two squared distances.
    |F_q - F_p|_infty <= 2 * bound on one squared-distance difference.
    """
    return 2.0 * squared_distance_perturbation_bound(eta, R)


def d_min_canonical() -> float:
    """Minimum pairwise distance between p_i(J_i), p_j(J_j) on support boxes."""
    boxes = tuple((float(lo), float(hi)) for lo, hi in KRAWCZYK_THETA_BOXES)
    return min(pairwise_separation_lower_bounds(boxes_from_fractions(boxes)))


def certified_eta0(boundary_margin: float) -> float:
    """Explicit perturbation radius with E(eta0) < m and eta0 < d_min/4."""
    R = R_max_on_support_boxes()
    dmin = d_min_canonical()
    m = boundary_margin
    eta_from_m = 0.9 * m / (16.0 * R)
    eta_from_sep = 0.24 * dmin
    eta = min(eta_from_m, eta_from_sep)
    # Round down to one significant digit below eta
    if eta <= 0:
        return 1e-9
    exp = int(math.floor(math.log10(eta)))
    scale = 10.0 ** exp
    eta_r = math.floor(eta / scale * 9.0) / 9.0 * scale
    return max(eta_r, 1e-9)


@dataclass
class C0RobustnessCertificate:
    R: float
    d_min: float
    boundary_margin: float
    E_eta0: float
    eta0: float
    side_length_lower_bound: float
    radius_lower_bound: float
    homotopy_boundary_excluded: bool

    def perturbation_sufficient(self) -> bool:
        return self.E_eta0 < self.boundary_margin and self.eta0 > 0


def build_c0_certificate(boundary_margin: float) -> C0RobustnessCertificate:
    boxes = tuple((float(lo), float(hi)) for lo, hi in KRAWCZYK_THETA_BOXES)
    ivs = boxes_from_fractions(boxes)
    eta0 = certified_eta0(boundary_margin)
    E = F_perturbation_bound(eta0)
    return C0RobustnessCertificate(
        R=R_max_on_support_boxes(),
        d_min=d_min_canonical(),
        boundary_margin=boundary_margin,
        E_eta0=E,
        eta0=eta0,
        side_length_lower_bound=side_length_lower_bound(ivs),
        radius_lower_bound=min_radius_lower_bound(ivs),
        homotopy_boundary_excluded=E < boundary_margin,
    )
