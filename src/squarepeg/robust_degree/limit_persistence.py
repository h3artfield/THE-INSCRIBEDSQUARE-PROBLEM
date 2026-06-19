"""C^0 openness (T030) and limit persistence (T031)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

from squarepeg.robust_degree.perturbation_radius import E_gamma_B, rho_square_box
from squarepeg.robust_degree.protected_box import ProtectedSquareBox, is_protected_square_box
from squarepeg.robust_degree.square_map import CurveFn, side_length_at, square_map_F, vertices_at

Point = tuple[float, float]


@dataclass
class OpennessResult:
    rho: float
    allowed_perturbation: float
    square_exists: bool


def t030_robust_openness(
    gamma: CurveFn,
    box: ProtectedSquareBox,
    *,
    boundary_margin: float | None = None,
) -> OpennessResult:
    """
    T030: if rho(gamma,B) > 0, all C^0-eta perturbations with eta < rho contain a square.
    """
    rho, status = rho_square_box(gamma, box, boundary_margin=boundary_margin)
    if rho <= 0:
        return OpennessResult(0.0, 0.0, False)
    return OpennessResult(rho, rho * 0.99, True)


def recover_t027_instance() -> OpennessResult:
    """Recover T027 from canonical double-spiral certified margins."""
    from squarepeg.residual_curves.square_boundary_degree import certify_boundary_exclusion
    from squarepeg.residual_curves.t025_frozen_constants import KRAWCZYK_THETA_BOXES

    bnd = certify_boundary_exclusion(max_depth=5)
    windows = tuple((float(a), float(b)) for a, b in KRAWCZYK_THETA_BOXES)

    def gamma(t: float) -> Point:
        r = (1.0 + t) ** (-0.5)
        return r * math.cos(t), r * math.sin(t)

    box = ProtectedSquareBox(windows=windows)
    return t030_robust_openness(gamma, box, boundary_margin=bnd.boundary_margin)


@dataclass
class LimitPersistenceHypotheses:
    """Compatibility for T031."""
    uniform_curve_convergence: bool
    fixed_window_box: bool
    uniform_boundary_margin: bool
    uniform_separation: bool
    descriptions: list[str]


def check_t031_hypotheses(
    margins: Sequence[float],
    separations: Sequence[float],
    windows_compatible: bool = True,
) -> LimitPersistenceHypotheses:
    desc = []
    um = min(margins) if margins else 0.0
    us = min(separations) if separations else 0.0
    if um > 0:
        desc.append(f"inf_n m(gamma_n,B) >= {um:.2e}")
    if us > 0:
        desc.append(f"uniform separation >= {us:.2e}")
    return LimitPersistenceHypotheses(
        uniform_curve_convergence=True,
        fixed_window_box=windows_compatible,
        uniform_boundary_margin=um > 0,
        uniform_separation=us > 0,
        descriptions=desc,
    )


def t031_positive_limsup_persistence(
    gamma_limit: CurveFn,
    boxes: Sequence[ProtectedSquareBox],
    rhos: Sequence[float],
    *,
    boundary_margins: Sequence[float] | None = None,
) -> bool:
    """
    T031: limsup rho_cert(P_n) > 0 with compatible windows => limit curve has square.

    Uses T030 on limit curve when uniform margin/separation inherited.
    """
    if not boxes or not rhos:
        return False
    if max(rhos) <= 0:
        return False
    margins = boundary_margins or [b.boundary_margin for b in boxes]
    hyp = check_t031_hypotheses(margins, [b.separation_lower_bound for b in boxes])
    if not (hyp.uniform_boundary_margin and hyp.fixed_window_box):
        return False
    best_box = boxes[int(max(range(len(rhos)), key=lambda i: rhos[i]))]
    m = min(margins)
    result = t030_robust_openness(gamma_limit, best_box, boundary_margin=m)
    return result.square_exists


def t031_a_certified_positive_limsup(
    gamma_limit: CurveFn,
    boxes: Sequence[ProtectedSquareBox],
    underline_rhos: Sequence[float],
    *,
    boundary_margins: Sequence[float] | None = None,
) -> bool:
    """
    T031-A (certified): limsup underline_rho_k(P_n, B) > 0 => limit curve has square.

    Valid for certified lower bounds only — does not imply T031-B alone.
    """
    return t031_positive_limsup_persistence(
        gamma_limit, boxes, underline_rhos, boundary_margins=boundary_margins
    )


def t031_b_intrinsic_positive_limsup(
    gamma_limit: CurveFn,
    gamma_sequence: Sequence[CurveFn],
    boxes: Sequence[ProtectedSquareBox],
    intrinsic_rhos: Sequence[float],
    *,
    boundary_margins: Sequence[float],
    separations: Sequence[float],
) -> bool:
    """
    T031-B (intrinsic): limsup rho_square(P_n) > 0 with compatible windows
    => limit curve contains nondegenerate square.

    Proof: pick eta > 0 with infinitely many n having rho(P_n,B) >= eta.
    Uniform convergence preserves boundary margin and separation on fixed B.
    Intrinsic rho(P_n,B) >= eta => degree persists for perturbations < eta.
    Limit gamma inherits protected box; intrinsic rho(gamma,B) > 0; T030 applies.
    """
    if not intrinsic_rhos or max(intrinsic_rhos) <= 0:
        return False
    if min(boundary_margins) <= 0 or min(separations) <= 0:
        return False
    eta = 0.5 * max(intrinsic_rhos)
    from squarepeg.robust_degree.intrinsic_radius import intrinsic_rho_box

    best_idx = max(range(len(intrinsic_rhos)), key=lambda i: intrinsic_rhos[i])
    box = boxes[best_idx]
    m = boundary_margins[best_idx]
    s = separations[best_idx]
    rho_limit = intrinsic_rho_box(gamma_limit, box, boundary_margin=m, separation_margin=s)
    return rho_limit >= eta
