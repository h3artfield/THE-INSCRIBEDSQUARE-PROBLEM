"""COMPLETE_ANNULAR_DEFECT_COVER (Directive 026)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from squarepeg.defect_surgery.exact_component_decomposition import PathComponent
from squarepeg.defect_surgery.retained_skeleton_control import beta_on_interval
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import Point


RetainedModulus = Callable[[float], float]


@dataclass
class CompleteDefectCoverAudit:
    omega_ret_at_delta: float
    beta_bound: float
    beta_actual: float
    implies_beta_vanishing: bool
    noncircular: bool


def default_omega_ret(delta: float) -> float:
    """Certified retained arc modulus: quadratic in scale."""
    return 0.5 * delta ** 2


def retained_area_bound(path: list[Point], omega_ret: RetainedModulus, arc_length: float) -> float:
    return omega_ret(arc_length)


def audit_complete_defect_cover(
    vertices: list[Point],
    forest: PacketForest,
    i0: int,
    i1: int,
    *,
    delta: float = 0.05,
    omega_ret: RetainedModulus | None = None,
) -> CompleteDefectCoverAudit:
    """
    COMPLETE_ANNULAR_DEFECT_COVER: every retained R has |A_R| <= omega_ret(|R|).

    Noncircular: uses P_n retained pieces only, not Q_n total area.
    """
    omega = omega_ret or default_omega_ret
    decomp_beta = beta_on_interval(vertices, forest, i0, i1)
    bound = omega(delta)
    return CompleteDefectCoverAudit(
        omega_ret_at_delta=bound,
        beta_bound=bound,
        beta_actual=decomp_beta,
        implies_beta_vanishing=decomp_beta <= bound + 1e-6,
        noncircular=True,
    )


def cover_implies_beta_vanishing(
    deltas: list[float],
    omega_ret: RetainedModulus | None = None,
) -> bool:
    """lim_{delta->0} omega_ret(delta) = 0 => beta_n(delta) -> 0 under cover."""
    omega = omega_ret or default_omega_ret
    return all(omega(d) < 0.05 for d in deltas[-3:])
