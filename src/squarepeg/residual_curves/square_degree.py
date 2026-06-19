"""Brouwer degree helpers for smooth square map (Directive 012)."""

from __future__ import annotations

from squarepeg.residual_curves.smooth_square_intervals import F_interval, IVal, contains_zero
from squarepeg.residual_curves.smooth_square_system import square_map_F_theta


def boundary_excluded(
    theta_boxes: list[tuple[float, float]],
    face: int,
    is_upper: bool,
) -> bool:
    """Check F != 0 on one face of parameter box via interval enclosure."""
    ivs = [IVal(lo, hi) for lo, hi in theta_boxes]
    lo, hi = theta_boxes[face]
    ivs[face] = IVal(hi, hi) if is_upper else IVal(lo, lo)
    F_iv = F_interval(tuple(ivs))  # type: ignore[arg-type]
    return all(not contains_zero(iv) for iv in F_iv)


def initial_degree_nonsingular(center: list[float]) -> float:
    """Sign of det J at polygon/chord root — placeholder for degree sum."""
    from squarepeg.residual_curves.smooth_square_intervals import _det4
    from squarepeg.residual_curves.smooth_square_system import jacobian_theta

    return _det4(jacobian_theta(center))
