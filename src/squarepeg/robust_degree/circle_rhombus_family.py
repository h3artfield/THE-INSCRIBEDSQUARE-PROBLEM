"""Unit circle ordered rhombus family calibration."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from squarepeg.robust_degree.rhombus_map import diagonal_defect_D, rhombus_map_G
from squarepeg.robust_degree.square_map import jacobian_F

# Expected DF at z(t) under frozen convention (Directive 018).
EXPECTED_DF_CIRCLE = np.array(
    [[-2.0, 4.0, -2.0, 0.0], [0.0, -2.0, 4.0, -2.0], [-2.0, 0.0, -2.0, 4.0], [0.0, 0.0, 0.0, 0.0]],
    dtype=float,
)

EXPECTED_DG_CIRCLE = EXPECTED_DF_CIRCLE[:3, :]
TANGENT_ALL_ONES = np.array([1.0, 1.0, 1.0, 1.0])


def circle_gamma(t: float) -> tuple[float, float]:
    return math.cos(t), math.sin(t)


def circle_family_param(t: float) -> tuple[float, float, float, float]:
    return (t, t + math.pi / 2, t + math.pi, t + 3 * math.pi / 2)


def circle_family_domain() -> tuple[float, float]:
    return (0.0, 2.0 * math.pi)


@dataclass
class CircleRhombusCalibration:
    rank_DF: int
    rank_DG: int
    kernel_equals_tangent: bool
    df_matches_expected: bool
    max_df_error: float
    G_zero_on_family: bool
    D_zero_on_family: bool
    notes: list[str]


def jacobian_G(gamma, u, eps: float = 1e-7) -> np.ndarray:
    g0 = rhombus_map_G(gamma, u)
    jac = np.zeros((3, 4))
    for j in range(4):
        up = list(u)
        up[j] += eps
        gj = rhombus_map_G(gamma, up)
        for i in range(3):
            jac[i, j] = (gj[i] - g0[i]) / eps
    return jac


def audit_circle_rhombus_family(t: float = 0.37) -> CircleRhombusCalibration:
    gamma = circle_gamma
    u = circle_family_param(t)
    df = np.array(jacobian_F(gamma, u))
    dg = jacobian_G(gamma, u)
    rank_df = int(np.linalg.matrix_rank(df, tol=1e-4))
    rank_dg = int(np.linalg.matrix_rank(dg, tol=1e-4))
    _, _, vh = np.linalg.svd(df)
    ker = vh[-1]
    ker = ker / np.linalg.norm(ker)
    ker_ok = abs(float(np.dot(ker, TANGENT_ALL_ONES))) > 0.99
    err = float(np.max(np.abs(df - EXPECTED_DF_CIRCLE)))
    g_max = 0.0
    d_max = 0.0
    for i in range(16):
        tt = 2 * math.pi * i / 15
        z = circle_family_param(tt)
        g = rhombus_map_G(gamma, z)
        g_max = max(g_max, max(abs(x) for x in g))
        d_max = max(d_max, abs(diagonal_defect_D(gamma, z)))
    return CircleRhombusCalibration(
        rank_DF=rank_df,
        rank_DG=rank_dg,
        kernel_equals_tangent=ker_ok,
        df_matches_expected=err < 1e-5,
        max_df_error=err,
        G_zero_on_family=g_max < 1e-8,
        D_zero_on_family=d_max < 1e-8,
        notes=[
            "rank DG = 3 on circle family; ker = span(1,1,1,1)",
            "Rhombus family transversely nondegenerate",
        ],
    )


def radial_component(gamma, h, t: float) -> float:
    """a(t) = gamma(t) · h(t) for gamma_ε = gamma + ε h."""
    x, y = gamma(t)
    hx, hy = h(t)
    return x * hx + y * hy


def first_order_diagonal_variation(
    h,
    t: float,
) -> float:
    """
    δD_h(t) = 4[a(t)+a(t+π) - a(t+π/2) - a(t+3π/2)] with a = γ·h on circle.
    """
    a = lambda tt: radial_component(circle_gamma, h, tt)
    return 4.0 * (a(t) + a(t + math.pi) - a(t + math.pi / 2) - a(t + 3 * math.pi / 2))


def verify_anti_periodicity_delta(h, t: float, tol: float = 1e-10) -> bool:
    d0 = first_order_diagonal_variation(h, t)
    d1 = first_order_diagonal_variation(h, t + math.pi / 2)
    return abs(d0 + d1) <= tol
