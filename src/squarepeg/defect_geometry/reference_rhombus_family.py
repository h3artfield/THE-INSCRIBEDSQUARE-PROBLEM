"""Rhombus family on reference annular curve."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from squarepeg.defect_geometry.reference_annulus import ReferenceAnnulus, default_reference_annulus, star_annular_gamma
from squarepeg.robust_degree.circle_rhombus_family import jacobian_G
from squarepeg.robust_degree.rhombus_map import diagonal_defect_D, rhombus_map_G


@dataclass
class ReferenceRhombusFamily:
    parametrization: str
    rank_dg: int
    g_zero_on_family: bool
    d_zero_on_family: bool
    side_margin: float
    tau_delta: float


def family_param(t: float) -> tuple[float, float, float, float]:
    return (t, t + math.pi / 2, t + math.pi, t + 3 * math.pi / 2)


def audit_reference_rhombus_family(spec: ReferenceAnnulus | None = None) -> ReferenceRhombusFamily:
    spec = spec or default_reference_annulus()
    gamma = star_annular_gamma(spec)
    g_max = 0.0
    d_max = 0.0
    ranks: list[int] = []
    for i in range(16):
        t = 2 * math.pi * i / 15
        u = family_param(t)
        g = rhombus_map_G(gamma, u)
        g_max = max(g_max, max(abs(x) for x in g))
        d_max = max(d_max, abs(diagonal_defect_D(gamma, u)))
        jac = jacobian_G(gamma, u)
        ranks.append(int(np.linalg.matrix_rank(jac, tol=1e-3)))
    rk = min(ranks) if ranks else 0
    # side margin from min side squared
    t0 = 0.0
    u0 = family_param(t0)
    pts = [gamma(ui) for ui in u0]
    sides = [math.hypot(pts[i][0] - pts[(i + 1) % 4][0], pts[i][1] - pts[(i + 1) % 4][1]) for i in range(4)]
    return ReferenceRhombusFamily(
        parametrization="z(t)=(t,t+pi/2,t+pi,t+3pi/2)",
        rank_dg=rk,
        g_zero_on_family=g_max < 1e-5,
        d_zero_on_family=d_max < 1e-5,
        side_margin=min(sides),
        tau_delta=math.pi / 2,
    )
