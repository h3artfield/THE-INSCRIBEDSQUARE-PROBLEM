"""Primitive obstruction for double-spiral area-tightness (T024)."""

from __future__ import annotations

import math

from squarepeg.residual_curves.canonical import (
    CANONICAL_THETA0,
    smooth_relative_area_outer_arm,
    tail_disk_radius,
    tail_interval_length,
)
from squarepeg.residual_curves.double_spiral import gamma_plus


def endpoint_chord_correction(m: float, n: float) -> float:
    """Endpoint term (1/2)[p_m, p_n] in relative area."""
    pm = gamma_plus(m)
    pn = gamma_plus(n)
    return 0.5 * (pm[0] * pn[1] - pn[0] * pm[1])


def endpoint_correction_bound(m: float, n: float) -> float:
    """Explicit bound: |chord| <= |p_m||p_n| sin(angle) <= |p_m||p_n|."""
    pm = gamma_plus(m)
    pn = gamma_plus(n)
    rm = math.hypot(pm[0], pm[1])
    rn = math.hypot(pn[0], pn[1])
    return rm * rn


def integral_half_r_squared(m: float, n: float) -> float:
    """(1/2) int_m^n r(theta)^2 dtheta = (1/2) log((1+n)/(1+m))."""
    if n <= m:
        return 0.0
    return 0.5 * math.log((1.0 + n) / (1.0 + m))


def relative_area_lower_bound(m: float, n: float) -> float:
    """
    |A(m,n)| >= (1/2)log((1+n)/(1+m)) - rm*rn for outer arm.
    """
    integral = integral_half_r_squared(m, n)
    bound = endpoint_correction_bound(m, n)
    return max(0.0, integral - bound)


def log_tail_lower_bound(m: float, *, ratio: float = 1.0) -> float:
    """
    For n = m^ratio with ratio >= 1: (1/2)log((1+n)/(1+m)) - 1/(1+m).
    Uses rm*rn <= r(m)^2 <= 1/(1+m) for crude bound.
    """
    n = m ** ratio
    integral = integral_half_r_squared(m, n)
    rm = math.hypot(*gamma_plus(m))
    err = rm * rm
    return max(0.0, integral - err)


def tail_obstructs_area_tightness(m: float, *, ratio: float = 2.0) -> dict:
    """
    Certificate that interval I_m = [t(m), t(m^ratio)] violates area-tightness
    when m is large: param length -> 0 but area lower bound -> infinity.
    """
    n = m ** ratio
    param_len = tail_interval_length(m, n)
    disk_r = tail_disk_radius(n)
    area_lb = log_tail_lower_bound(m, ratio=ratio)
    smooth = abs(smooth_relative_area_outer_arm(m, n))
    return {
        "M": m,
        "N": n,
        "param_interval_length": param_len,
        "tail_disk_radius": disk_r,
        "area_lower_bound": area_lb,
        "smooth_relative_area": smooth,
        "endpoint_bound": endpoint_correction_bound(m, n),
        "obstructs": area_lb > 0.1 and param_len < 0.5,
    }


def primitive_equicontinuity_contradiction(
    m: float,
    *,
    ratio: float = 2.0,
    omega_bound: float = 0.01,
) -> bool:
    """
    If |s-t| = param_len and |A(s,t)| >= area_lb >> omega_bound,
    uniform primitive convergence is impossible.
    """
    n = m ** ratio
    param_len = tail_interval_length(m, n)
    area_lb = log_tail_lower_bound(m, ratio=ratio)
    endpoint = endpoint_correction_bound(m, n)
    return area_lb > omega_bound + endpoint and param_len < 0.25
