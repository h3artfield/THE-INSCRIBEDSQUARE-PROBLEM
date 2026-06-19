"""Two-invariant Level-F model with indexed duality."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

from squarepeg.spectral_axioms.grid_model import GridLPConfig


@dataclass
class TwoInvariantConfig:
    N: int
    kappa: Fraction
    k: int = 1
    delta: Fraction = Fraction(0)


@dataclass
class TwoInvariantResult:
    config: TwoInvariantConfig
    g1_values: list[Fraction]
    g2_values: list[Fraction]
    optimum_g2_midpoint: Fraction
    status: str
    message: str


def _add_invariant_constraints(
    A_ub: list,
    b_ub: list,
    A_eq: list,
    b_eq: list,
    offset: int,
    N: int,
    kappa: float,
    delta: float,
    endpoint_lo: float,
    endpoint_hi: float,
) -> None:
    n = N + 1
    row0 = [0.0] * (2 * n)
    row0[offset] = 1.0
    A_eq.append(row0)
    b_eq.append(endpoint_lo)
    row1 = [0.0] * (2 * n)
    row1[offset + N] = 1.0
    A_eq.append(row1)
    b_eq.append(endpoint_hi)

    for i in range(N):
        row = [0.0] * (2 * n)
        row[offset + i] = 1.0
        row[offset + i + 1] = -1.0
        A_ub.append(row)
        b_ub.append(-delta)

    for i in range(N + 1):
        for j in range(i + 1, N + 1):
            row = [0.0] * (2 * n)
            row[offset + i] = -1.0
            row[offset + j] = 1.0
            A_ub.append(row)
            b_ub.append(kappa * (j - i) / N)

    for i in range(N + 1):
        for j in range(N + 1 - i):
            s = i + j
            if s > N:
                continue
            row = [0.0] * (2 * n)
            row[offset + s] = 1.0
            row[offset + i] -= 1.0
            row[offset + j] -= 1.0
            A_ub.append(row)
            b_ub.append(0.0)


def solve_two_invariant(config: TwoInvariantConfig) -> TwoInvariantResult:
    """
    Minimize g2 midpoint slope subject to Level-F on g1, g2, and indexed duality:
    g1(x) + g2(1-x) = 1  at grid points x_i = i/N.
    """
    N = config.N
    k = config.k
    kappa = float(config.kappa)
    delta = float(config.delta)
    n = N + 1
    total = 2 * n

    c = np.zeros(total)
    half = N // 2
    scale = N / (2 * k)
    c[n + half + k] = scale
    c[n + half - k] = -scale

    A_ub: list = []
    b_ub: list = []
    A_eq: list = []
    b_eq: list = []

    _add_invariant_constraints(A_ub, b_ub, A_eq, b_eq, 0, N, kappa, delta, 0.0, 1.0)
    _add_invariant_constraints(A_ub, b_ub, A_eq, b_eq, n, N, kappa, delta, 0.0, 1.0)

    # Indexed duality: G1_i + G2_{N-i} = 1
    for i in range(N + 1):
        row = [0.0] * total
        row[i] = 1.0
        row[n + (N - i)] = 1.0
        A_eq.append(row)
        b_eq.append(1.0)

    bounds = [(0.0, 1.0)] * total
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
        return TwoInvariantResult(
            config=config,
            g1_values=[],
            g2_values=[],
            optimum_g2_midpoint=Fraction(-1),
            status="failed",
            message=res.message,
        )

    g1 = [Fraction(v).limit_denominator(10**8) for v in res.x[:n]]
    g2 = [Fraction(v).limit_denominator(10**8) for v in res.x[n:]]
    opt = Fraction(res.fun).limit_denominator(10**8)
    return TwoInvariantResult(
        config=config,
        g1_values=g1,
        g2_values=g2,
        optimum_g2_midpoint=opt,
        status="optimal",
        message=res.message,
    )
