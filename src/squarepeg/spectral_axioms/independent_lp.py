"""Independent LP replication (no imports from grid_model)."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.optimize import linprog


def build_constraints_independent(N: int, kappa: float, delta: float = 0.0):
    """Replicate Level-F LP from first principles."""
    n = N + 1
    A_eq, b_eq, A_ub, b_ub = [], [], [], []

    e0 = [0.0] * n
    e0[0] = 1.0
    A_eq.append(e0)
    b_eq.append(0.0)
    e1 = [0.0] * n
    e1[N] = 1.0
    A_eq.append(e1)
    b_eq.append(1.0)

    for i in range(N):
        row = [0.0] * n
        row[i] = 1.0
        row[i + 1] = -1.0
        A_ub.append(row)
        b_ub.append(-delta)

    for i in range(n):
        for j in range(i + 1, n):
            row = [0.0] * n
            row[i] = -1.0
            row[j] = 1.0
            A_ub.append(row)
            b_ub.append(kappa * (j - i) / N)

    for i in range(n):
        for j in range(n - i):
            s = i + j
            if s > N:
                continue
            row = [0.0] * n
            row[s] = 1.0
            row[i] -= 1.0
            row[j] -= 1.0
            A_ub.append(row)
            b_ub.append(0.0)

    return A_ub, b_ub, A_eq, b_eq


def objective_midpoint(N: int, k: int) -> np.ndarray:
    c = np.zeros(N + 1)
    half = N // 2
    scale = N / (2 * k)
    c[half + k] = scale
    c[half - k] = -scale
    return c


def solve_independent(N: int, kappa: Fraction, k: int = 1, delta: float = 0.0) -> dict:
    c = objective_midpoint(N, k)
    A_ub, b_ub, A_eq, b_eq = build_constraints_independent(N, float(kappa), delta)
    res = linprog(
        c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(0.0, 1.0)] * (N + 1),
        method="highs",
    )
    if not res.success:
        return {"success": False, "message": res.message}
    values = [Fraction(v).limit_denominator(10**8) for v in res.x]
    opt = Fraction(res.fun).limit_denominator(10**8)
    return {"success": True, "optimum": opt, "values": values, "message": res.message}


def compare_with_primary(
    primary_values: list[Fraction],
    primary_opt: Fraction,
    N: int,
    kappa: Fraction,
    k: int = 1,
) -> dict:
    ind = solve_independent(N, kappa, k)
    if not ind["success"]:
        return {"match": False, "reason": "independent infeasible"}
    same_opt = ind["optimum"] == primary_opt
    same_vals = ind["values"] == primary_values
    return {
        "match_optimum": same_opt,
        "match_values": same_vals,
        "independent_optimum": str(ind["optimum"]),
        "primary_optimum": str(primary_opt),
    }
