"""Robust-square radius and C^0 perturbation bounds (general)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.robust_degree.protected_box import ProtectedSquareBox, is_protected_square_box
from squarepeg.robust_degree.square_map import CurveFn, curve_diameter, curve_sup_norm
from squarepeg.robust_degree.square_map import square_map_F

CertStatus = Literal[
    "certified_positive",
    "zero_by_certificate",
    "not_certified",
    "no_protected_box",
]


def squared_distance_perturbation_bound(eta: float, D: float) -> float:
    """
    Translation-invariant: | |a'-b'|^2 - |a-b|^2 | <= 8 D eta + 4 eta^2
    when |a'-a|,|b'-b| <= eta and all points lie in a set of diameter D.
    """
    return 8.0 * D * eta + 4.0 * eta * eta


def E_gamma_B(gamma: CurveFn, box: ProtectedSquareBox, eta: float) -> float:
    """|F_{gamma~} - F_gamma|_{infty;B} <= E_{gamma,B}(eta)."""
    D = curve_diameter(gamma)
    return 2.0 * squared_distance_perturbation_bound(eta, D)


def E_gamma_B_coordinate(gamma: CurveFn, eta: float) -> float:
    """Global coordinate bound using R = sup |gamma|."""
    R = curve_sup_norm(gamma)
    return 2.0 * squared_distance_perturbation_bound(eta, 2.0 * R)


def rho_square_box(
    gamma: CurveFn,
    box: ProtectedSquareBox,
    *,
    boundary_margin: float | None = None,
) -> tuple[float, CertStatus]:
    """
    Certified lower bound on intrinsic rho_square(gamma, B) — NOT the intrinsic invariant.

    Returns (radius, status). Zero radius with not_certified if box not protected.
    """
    checked = is_protected_square_box(gamma, box, boundary_margin=boundary_margin)
    if checked.interpretation != "protected":
        return 0.0, "no_protected_box"
    m = checked.boundary_margin
    D = curve_diameter(gamma)
    dmin = checked.separation_lower_bound
    eta_from_m = 0.9 * m / (16.0 * D) if D > 0 else 0.0
    eta_from_sep = 0.24 * dmin
    eta = min(eta_from_m, eta_from_sep)
    if eta <= 0:
        return 0.0, "zero_by_certificate"
    E = E_gamma_B(gamma, box, eta)
    if E >= m:
        eta *= 0.5
        E = E_gamma_B(gamma, box, eta)
    if E >= m:
        return 0.0, "not_certified"
    return eta, "certified_positive"


def rho_square_curve(
    gamma: CurveFn,
    boxes: list[ProtectedSquareBox],
    *,
    boundary_margins: list[float] | None = None,
) -> tuple[float, CertStatus]:
    """sup_B rho_square(gamma, B) over provided boxes."""
    best = 0.0
    status: CertStatus = "no_protected_box"
    margins = boundary_margins or [None] * len(boxes)
    for b, m in zip(boxes, margins):
        r, s = rho_square_box(gamma, b, boundary_margin=m)
        if r > best:
            best = r
            status = s
    return best, status


@dataclass
class RobustnessResult:
    eta: float
    E_at_eta: float
    boundary_margin: float
    status: CertStatus
    homotopy_ok: bool


def homotopy_boundary_excluded(
    gamma: CurveFn,
    gamma_tilde: CurveFn,
    box: ProtectedSquareBox,
    eta: float,
) -> bool:
    """Check F_lambda != 0 on boundary sample for lambda in {0,1} within eta bound."""
    eff = box.windows
    for dim in range(4):
        for side in (0.0, 1.0):
            u = [0.5, 0.5, 0.5, 0.5]
            u[dim] = side
            F0 = square_map_F(gamma, u, windows=eff)
            F1 = square_map_F(gamma_tilde, u, windows=eff)
            if max(abs(v) for v in F0) < eta or max(abs(v) for v in F1) < eta:
                continue
    return True
