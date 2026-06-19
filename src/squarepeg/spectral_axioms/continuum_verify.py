"""Continuum verification of countermodels and subadditivity."""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from typing import TypeAlias

Number = Fraction | int | float
Func: TypeAlias = Callable[[float], float]


def grid_pl_function(values: list[Fraction], N: int) -> Func:
    """Piecewise-linear interpolation of grid values G_i at x_i = i/N."""
    xs = [float(i / N) for i in range(N + 1)]
    ys = [float(v) for v in values]

    def g(x: float) -> float:
        if x <= 0.0:
            return 0.0
        if x >= 1.0:
            return 1.0
        i = min(int(x * N), N - 1)
        denom = xs[i + 1] - xs[i]
        t = (x - xs[i]) / denom if denom else 0.0
        return ys[i] + t * (ys[i + 1] - ys[i])

    return g


def verify_endpoints(g: Func, tol: float = 1e-12) -> bool:
    return abs(g(0.0)) <= tol and abs(g(1.0) - 1.0) <= tol


def verify_monotone(g: Func, samples: int = 2000) -> bool:
    xs = [i / samples for i in range(samples + 1)]
    return all(g(xs[i + 1]) + 1e-12 >= g(xs[i]) for i in range(samples))


def verify_lipschitz(g: Func, kappa: float, samples: int = 2000) -> bool:
    xs = [i / samples for i in range(samples + 1)]
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if g(xs[j]) - g(xs[i]) > kappa * (xs[j] - xs[i]) + 1e-9:
                return False
    return True


def verify_subadditive_grid(g: Func, M: int = 500) -> bool:
    """Check g(x+y) <= g(x)+g(y) on the rational grid {0,1/M,...,1}."""
    xs = [i / M for i in range(M + 1)]
    for x in xs:
        for y in xs:
            if x + y <= 1.0 + 1e-15:
                if g(x + y) > g(x) + g(y) + 1e-9:
                    return False
    return True


def verify_subadditive_piecewise_linear(
    breakpoints: list[tuple[Fraction, Fraction]],
    M: int = 500,
) -> tuple[bool, list[tuple[Fraction, Fraction, Fraction]]]:
    """
    Verify subadditivity on a dense rational grid for a PL function.
    """
    xs = sorted({bp[0] for bp in breakpoints})
    x0, y0 = breakpoints[0]
    segments: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    for i in range(len(breakpoints) - 1):
        xa, ya = breakpoints[i]
        xb, yb = breakpoints[i + 1]
        slope = (yb - ya) / (xb - xa) if xb != xa else Fraction(0)
        segments.append((xa, xb, ya, slope))

    def g_at(x: Fraction) -> Fraction:
        if x <= x0:
            return y0
        for xa, xb, ya, slope in segments:
            if xa <= x <= xb:
                return ya + slope * (x - xa)
        return breakpoints[-1][1]

    grid = [Fraction(i, M) for i in range(M + 1)]
    violations: list[tuple[Fraction, Fraction, Fraction]] = []
    for x in grid:
        for y in grid:
            if x + y > Fraction(1):
                continue
            if g_at(x + y) > g_at(x) + g_at(y):
                violations.append((x, y, x + y))
    return len(violations) == 0, violations


def midpoint_quotient_fn(g: Func, h: float) -> float:
    return (g(0.5 + h) - g(0.5 - h)) / (2 * h)


def D_plus_numeric(g: Func, hs: list[float] | None = None) -> float:
    if hs is None:
        hs = [0.5**k for k in range(3, 20)]
    return max(midpoint_quotient_fn(g, h) for h in hs if h < 0.5)


def certify_grid_witness(
    values: list[Fraction],
    N: int,
    kappa: float,
    subadd_M: int = 500,
    k: int = 1,
) -> dict:
    """Certify a grid LP witness as a continuum PL countermodel."""
    g = grid_pl_function(values, N)
    h = k / N
    d_plus = midpoint_quotient_fn(g, h)
    return {
        "N": N,
        "kappa": kappa,
        "k": k,
        "endpoints": verify_endpoints(g),
        "monotone": verify_monotone(g),
        "lipschitz": verify_lipschitz(g, kappa),
        "subadditive_M": subadd_M,
        "subadditive": verify_subadditive_grid(g, subadd_M),
        "D_plus": d_plus,
    }
