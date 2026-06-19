"""Ellipse cyclic-odd rhombus audit."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

from squarepeg.robust_degree.circle_rhombus_family import jacobian_G
from squarepeg.robust_degree.rhombus_map import rhombus_map_G

EllipseStatus = Literal[
    "CYCLIC_ODD_CERTIFIED",
    "UNPROTECTED",
    "UNRESOLVED",
    "DEGENERATE_LIMIT",
]


@dataclass
class EllipseRhombusAudit:
    a: float
    b: float
    rank_dg_on_family: int
    G_zero_on_rotating_family: bool
    status: EllipseStatus
    notes: list[str]


def ellipse_gamma(a: float, b: float):
    def g(t: float) -> tuple[float, float]:
        return a * math.cos(t), b * math.sin(t)

    return g


def ellipse_rotating_family(a: float, b: float, n: int = 16) -> EllipseRhombusAudit:
    gamma = ellipse_gamma(a, b)
    g_max = 0.0
    ranks: list[int] = []
    for i in range(n):
        t = 2 * math.pi * i / n
        u = (t, t + math.pi / 2, t + math.pi, t + 3 * math.pi / 2)
        g = rhombus_map_G(gamma, u)
        g_max = max(g_max, max(abs(x) for x in g))
        jac = jacobian_G(gamma, u)
        ranks.append(int(np.linalg.matrix_rank(jac, tol=1e-4)))
    rk = min(ranks) if ranks else 0
    g_zero = g_max < 1e-6
    if a == b and g_zero and rk >= 3:
        status: EllipseStatus = "CYCLIC_ODD_CERTIFIED"
    elif b / a < 0.01:
        status = "DEGENERATE_LIMIT"
    elif g_zero:
        status = "UNRESOLVED"
    else:
        status = "UNPROTECTED"
    return EllipseRhombusAudit(
        a=a,
        b=b,
        rank_dg_on_family=rk,
        G_zero_on_rotating_family=g_zero,
        status=status,
        notes=[
            "Circle (a=b) inherits cyclic-odd certificate",
            "Large eccentricity may change family dimension — not assumed equal to circle",
        ],
    )
