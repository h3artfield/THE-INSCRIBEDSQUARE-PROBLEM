"""Area-tight subsequence selection (T035) and quantifier audit."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

from squarepeg.robust_degree.area_defect import alpha_P_delta, alpha_sequence_limsup

CurveFn = Callable[[float], tuple[float, float]]


def delta_grid(j: int) -> float:
    return 2.0 ** (-j)


@dataclass
class AreaTightSubsequenceCriterion:
    """T035: equivalent diagonal formulation."""

    delta_j: float
    epsilon_j: float


def alpha_n_delta(gamma: CurveFn, delta: float) -> float:
    return alpha_P_delta(gamma, delta)


def is_area_tight_subsequence(
    alphas: Sequence[Callable[[float], float]],
    indices: Sequence[int],
    *,
    tol: float = 1e-2,
) -> bool:
    """
    (P_{n_k}) area-tight iff lim_{delta->0} limsup_k alpha_{n_k}(delta) = 0.
    """
    if not indices:
        return False
    for delta in [0.25, 0.125, 0.0625, 0.03125]:
        vals = [alphas[i](delta) for i in indices if i < len(alphas)]
        if vals and max(vals[-3:]) > tol:
            return False
    return True


def diagonal_criterion_satisfied(
    alpha_at_n: Sequence[Callable[[float], float]],
    n_sequence: Sequence[int],
) -> bool:
    """
    T035 diagonal: exists increasing n_k with alpha_{n_k}(delta_j) < 2^{-j} for all j <= k.

    For k-th term, require alpha_{n_k}(delta_j) < 2^{-j} for j = 1..k.
    """
    if not n_sequence:
        return False
    for k, nk in enumerate(n_sequence):
        if nk >= len(alpha_at_n):
            return False
        for j in range(1, k + 2):
            if alpha_at_n[nk](delta_grid(j)) >= delta_grid(j):
                return False
    return True


def t035_equivalence_statement() -> dict[str, str]:
    return {
        "area_tight": (
            "Subsequence (P_{n_k}) is area-tight iff "
            "lim_{delta->0} limsup_{k->infty} alpha_{n_k}(delta) = 0."
        ),
        "diagonal": (
            "Equivalent: exists increasing (n_k) such that for each j, "
            "limsup_{k->infty} alpha_{n_k}(2^{-j}) = 0; "
            "constructive form: alpha_{n_k}(2^{-j}) < 2^{-j} for all j <= k."
        ),
        "negation": (
            "NOT area-tight: forall increasing (n_k), exists j with "
            "limsup_k alpha_{n_k}(2^{-j}) > 0. "
            "Defect may migrate among scales — no single fixed delta suffices."
        ),
    }


def negation_not_fixed_scale() -> str:
    return (
        "Failure of every area-tight subsequence does NOT imply "
        "alpha_n(delta_j) >= epsilon for all large n at one fixed j. "
        "Obstruction may migrate among scales delta_j."
    )
