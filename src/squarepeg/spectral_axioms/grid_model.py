"""Rational grid LP for Level-F spectral axioms."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

import numpy as np
from scipy.optimize import linprog

Number = Fraction | int | float


@dataclass
class GridLPConfig:
    N: int
    kappa: Fraction
    k: int = 1
    delta: Fraction = Fraction(0)
    strict_monotone: bool = False


@dataclass
class GridLPResult:
    config: GridLPConfig
    optimum: Fraction
    values: list[Fraction]
    status: str
    scipy_message: str
    verified: bool = False
    verification_errors: list[str] = field(default_factory=list)
    dual_bound: Fraction | None = None


def grid_points(N: int) -> list[Fraction]:
    return [Fraction(i, N) for i in range(N + 1)]


def midpoint_objective_coeffs(N: int, k: int) -> np.ndarray:
    """Minimize D_{N,k} = (G_{N/2+k} - G_{N/2-k}) / (2k/N)."""
    c = np.zeros(N + 1)
    half = N // 2
    scale = N / (2 * k)
    c[half + k] = scale
    c[half - k] = -scale
    return c


def build_level_f_lp(config: GridLPConfig):
    """Build scipy linprog (min c^T x s.t. A_ub x <= b_ub, A_eq x = b_eq)."""
    N = config.N
    kappa = float(config.kappa)
    k = config.k
    delta = float(config.delta)
    n = N + 1

    c = midpoint_objective_coeffs(N, k)

    A_eq: list[list[float]] = []
    b_eq: list[float] = []
    A_ub: list[list[float]] = []
    b_ub: list[float] = []

    # Endpoints
    row0 = [0.0] * n
    row0[0] = 1.0
    A_eq.append(row0)
    b_eq.append(0.0)
    row1 = [0.0] * n
    row1[N] = 1.0
    A_eq.append(row1)
    b_eq.append(1.0)

    # Monotonicity G_{i+1} - G_i >= delta  =>  G_i - G_{i+1} <= -delta
    for i in range(N):
        row = [0.0] * n
        row[i] = 1.0
        row[i + 1] = -1.0
        A_ub.append(row)
        b_ub.append(-float(delta))

    # Lipschitz: G_j - G_i <= kappa * (j-i)/N
    for i in range(N + 1):
        for j in range(i + 1, N + 1):
            row = [0.0] * n
            row[i] = -1.0
            row[j] = 1.0
            A_ub.append(row)
            b_ub.append(kappa * (j - i) / N)

    # Triangle inequality: G_{i+j} <= G_i + G_j  =>  G_{i+j} - G_i - G_j <= 0
    for i in range(N + 1):
        for j in range(N + 1 - i):
            s = i + j
            if s > N:
                continue
            row = [0.0] * n
            row[s] = 1.0
            row[i] -= 1.0
            row[j] -= 1.0
            A_ub.append(row)
            b_ub.append(0.0)

    bounds = [(0.0, 1.0)] * n
    return c, A_ub, b_ub, A_eq, b_eq, bounds


def solve_grid_lp(config: GridLPConfig) -> GridLPResult:
    c, A_ub, b_ub, A_eq, b_eq, bounds = build_level_f_lp(config)
    res = linprog(
        c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs",
    )
    if not res.success:
        return GridLPResult(
            config=config,
            optimum=Fraction(-1),
            values=[],
            status="infeasible_or_failed",
            scipy_message=res.message,
        )

    values = [Fraction(v).limit_denominator(10**8) for v in res.x]
    opt = Fraction(res.fun).limit_denominator(10**8)
    return GridLPResult(
        config=config,
        optimum=opt,
        values=values,
        status="optimal",
        scipy_message=res.message,
    )


def verify_level_f(values: list[Fraction], config: GridLPConfig) -> tuple[bool, list[str]]:
    """Exact rational verification of all Level-F constraints."""
    from squarepeg.spectral_axioms.exact_verify import verify_grid_solution

    return verify_grid_solution(values, config)
