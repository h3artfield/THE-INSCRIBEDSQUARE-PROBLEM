"""Critical modulus functions and vanishing 2-variation checks."""

from __future__ import annotations

import math


def log_modulus(r: float, alpha: float) -> float:
    """m(r) = (log(e/r))^{-alpha}, alpha > 1/2 for integral condition."""
    if r <= 0:
        return float("inf")
    return 1.0 / (math.log(math.e / r) ** alpha)


def modulus_integral_finite(alpha: float, upper: float = 1.0) -> bool:
    """Numerical check int_0^1 m(r)^2/r dr < infinity (exploratory)."""
    if alpha <= 0.5:
        return False
    n = 10000
    total = 0.0
    for i in range(1, n + 1):
        r = upper * i / n
        m = log_modulus(r, alpha)
        total += (m * m / r) * (upper / n)
    return math.isfinite(total) and total < 1e6


def vanishing_2_var_bound(m_delta: float, m_val: float) -> float:
    """Upper bound omega_2(c, delta) <= M * m(delta)."""
    return m_val * m_delta
