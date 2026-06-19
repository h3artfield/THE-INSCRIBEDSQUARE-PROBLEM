"""Lyapunov–Schmidt reduced obstruction section s_H : Z -> E."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np

from squarepeg.robust_degree.cokernel_bundle import cokernel_covector, df_matrix
from squarepeg.robust_degree.square_map import CurveFn

PerturbationFn = Callable[[Sequence[float]], Sequence[float]]


@dataclass
class ObstructionSection:
    """Reduced section s_H(t) = pi_{E_t}(H(z(t))) after normal equations solved."""

    values: list[float]
    parameters: list[float]
    has_zero: bool
    max_abs: float


@dataclass
class ReducedZeroCriterion:
    """
    G = F + H has a zero near Z iff reduced section s_H vanishes somewhere on Z.

    First-order model: s_H = pi_E(H|_Z). Full LS reduction requires tubular neighborhood.
    """

    first_order_valid: bool
    statement: str


def project_to_cokernel(jac: np.ndarray, perturbation: Sequence[float]) -> float:
    ell = cokernel_covector(jac)
    h = np.array(perturbation, dtype=float)
    return float(np.dot(ell, h))


def obstruction_section_along_curve(
    gamma: CurveFn,
    parametrization: Callable[[float], tuple[float, float, float, float]],
    perturbation: PerturbationFn,
    ts: Sequence[float],
    *,
    eps: float = 1e-7,
) -> ObstructionSection:
    """
    Compute s_H(t) = ell_t^T H(u(t)) where H is additive perturbation of F-values.
    """
    values: list[float] = []
    for t in ts:
        u = parametrization(float(t))
        jac = df_matrix(gamma, u, eps=eps)
        h = perturbation(u)
        values.append(project_to_cokernel(jac, h))
    max_abs = max(abs(v) for v in values) if values else 0.0
    has_zero = any(abs(v) < 1e-9 for v in values) or (
        len(values) >= 2 and any(values[i] * values[j] <= 0 for i in range(len(values)) for j in range(i + 1, len(values)))
    )
    return ObstructionSection(
        values=values,
        parameters=list(ts),
        has_zero=has_zero,
        max_abs=max_abs,
    )


def constant_cokernel_section_removes_family(
    gamma: CurveFn,
    parametrization: Callable[[float], tuple[float, float, float, float]],
    eps: float,
    ts: Sequence[float],
) -> bool:
    """
    Constant perturbation eps along cokernel direction removes zeros iff eps != 0.
    """

    def cokernel_aligned_perturbation(u: Sequence[float]) -> list[float]:
        jac = df_matrix(gamma, u)
        ell = cokernel_covector(jac)
        return list(eps * ell)

    sec = obstruction_section_along_curve(
        gamma,
        parametrization,
        cokernel_aligned_perturbation,
        ts,
    )
    return all(abs(v - eps) < 1e-4 for v in sec.values)


def reduced_zero_criterion_statement() -> ReducedZeroCriterion:
    return ReducedZeroCriterion(
        first_order_valid=True,
        statement=(
            "For G = F + H with ||H|| small on tubular neighborhood N(Z), "
            "G^{-1}(0) cap N(Z) is nonempty iff the Lyapunov–Schmidt section "
            "s_H : Z -> E has a zero. Constant nonzero section in coker(DF) "
            "removes the family (see countermodel)."
        ),
    )
