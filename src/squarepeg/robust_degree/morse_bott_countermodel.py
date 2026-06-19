"""Morse–Bott persistence countermodel F(x,y) = (x, 0)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

CountermodelVerdict = Literal[
    "NORMAL_NONDEGENERACY_INSUFFICIENT",
    "UNRESOLVED",
]


@dataclass
class CountermodelAudit:
    """Audit of F(x,y) = (x, 0) showing normal index does not imply persistence."""

    zero_set_dim: int
    kernel_dim: int
    rank_df: int
    cokernel_dim: int
    normal_invertible: bool
    normal_degree_nonzero: bool
    persists_under_perturbation: bool
    verdict: CountermodelVerdict
    notes: list[str]


def F_countermodel(x: float, y: float) -> tuple[float, float]:
    return (x, 0.0)


def F_countermodel_perturbed(x: float, y: float, eps: float) -> tuple[float, float]:
    return (x, eps)


def jacobian_countermodel(_x: float, _y: float) -> list[list[float]]:
    return [[1.0, 0.0], [0.0, 0.0]]


def has_zero(x: float, y: float, eps: float = 0.0, tol: float = 1e-12) -> bool:
    fx, fy = F_countermodel_perturbed(x, y, eps)
    return abs(fx) <= tol and abs(fy) <= tol


def audit_countermodel() -> CountermodelAudit:
    """
    Z = {(0, y) : y in R} is 1D; ker DF = span(e_y); normal x-direction is iso.

    For eps != 0, F_eps has no zero — normal nondegeneracy does not force persistence.
    """
    jac = jacobian_countermodel(0.0, 0.0)
    rank = 1
    unperturbed_has_line = has_zero(0.0, 0.0)
    eps_values = [1e-3, -1e-3, 1e-6]
    perturbed_any_zero = any(has_zero(x, y, eps=e) for e in eps_values for x in (-1.0, 0.0, 1.0) for y in (-1.0, 0.0, 1.0))

    return CountermodelAudit(
        zero_set_dim=1,
        kernel_dim=1,
        rank_df=rank,
        cokernel_dim=1,
        normal_invertible=True,
        normal_degree_nonzero=True,
        persists_under_perturbation=unperturbed_has_line and not perturbed_any_zero,
        verdict="NORMAL_NONDEGENERACY_INSUFFICIENT",
        notes=[
            "ker DF = T Z at (0,y)",
            "Normal (x) derivative is 1 — nonzero 1D normal degree",
            "F_eps(x,y) = (x, eps) has empty zero set for eps != 0",
            "Obstruction lies in coker(DF) = y-equation; constant section eps removes family",
        ],
    )


def countermodel_theorem_statement() -> str:
    return (
        "Normal nondegeneracy or a nonzero fiberwise normal degree does not alone imply "
        "persistence of a positive-dimensional zero family under arbitrary small C^0 perturbations."
    )
