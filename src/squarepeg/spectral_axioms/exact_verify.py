"""Exact rational verification of grid LP solutions."""

from __future__ import annotations

from fractions import Fraction

from squarepeg.spectral_axioms.grid_model import GridLPConfig


def verify_grid_solution(
    values: list[Fraction], config: GridLPConfig
) -> tuple[bool, list[str]]:
    N = config.N
    kappa = Fraction(config.kappa)
    delta = Fraction(config.delta)
    errors: list[str] = []

    if len(values) != N + 1:
        errors.append(f"expected {N + 1} values, got {len(values)}")
        return False, errors

    if values[0] != 0:
        errors.append(f"G_0 = {values[0]}, expected 0")
    if values[N] != 1:
        errors.append(f"G_N = {values[N]}, expected 1")

    for i in range(N):
        diff = values[i + 1] - values[i]
        if diff < delta:
            errors.append(f"monotonicity fail at {i}: G_{i+1}-G_{i}={diff} < {delta}")

    for i in range(N + 1):
        for j in range(i + 1, N + 1):
            upper = kappa * Fraction(j - i, N)
            diff = values[j] - values[i]
            if diff > upper:
                errors.append(
                    f"Lipschitz fail ({i},{j}): G_{j}-G_{i}={diff} > {upper}"
                )

    for i in range(N + 1):
        for j in range(N + 1 - i):
            s = i + j
            if s > N:
                continue
            lhs = values[s]
            rhs = values[i] + values[j]
            if lhs > rhs:
                errors.append(
                    f"triangle fail ({i},{j}): G_{s}={lhs} > G_{i}+G_{j}={rhs}"
                )

    return len(errors) == 0, errors


def verify_midpoint_objective(
    values: list[Fraction], config: GridLPConfig
) -> Fraction:
    N, k = config.N, config.k
    half = N // 2
    return (values[half + k] - values[half - k]) / (2 * Fraction(k, N))
