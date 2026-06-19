"""Cyclic relabeling equivariance for rhombus and diagonal maps."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from squarepeg.robust_degree.rhombus_map import diagonal_defect_D, rhombus_map_G
from squarepeg.robust_degree.square_map import CurveFn

Param4 = tuple[float, float, float, float]

# G(tau u) = A @ G(u)
CYCLIC_A: np.ndarray = np.array(
    [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [-1.0, -1.0, -1.0]],
    dtype=float,
)


def cyclic_tau(u: Sequence[float]) -> Param4:
    return (float(u[1]), float(u[2]), float(u[3]), float(u[0]))


def verify_A_properties(tol: float = 1e-12) -> tuple[bool, bool, float]:
    """Returns (A^4 = I, det A = -1, ||A^4 - I||)."""
    a4 = np.linalg.matrix_power(CYCLIC_A, 4)
    err = float(np.linalg.norm(a4 - np.eye(3)))
    return err <= tol, abs(float(np.linalg.det(CYCLIC_A)) + 1.0) <= tol, err


@dataclass
class CyclicEquivarianceAudit:
    G_equivariant: bool
    D_anti_equivariant: bool
    A_fourth_power_error: float
    det_A: float
    max_G_error: float
    max_D_anti_error: float


def audit_cyclic_equivariance(
    gamma: CurveFn,
    samples: list[Param4],
) -> CyclicEquivarianceAudit:
    a4_ok, det_ok, a4_err = verify_A_properties()
    g_err = 0.0
    d_err = 0.0
    for u in samples:
        g0 = np.array(rhombus_map_G(gamma, u))
        g1 = np.array(rhombus_map_G(gamma, cyclic_tau(u)))
        g_err = max(g_err, float(np.linalg.norm(g1 - CYCLIC_A @ g0)))
        d0 = diagonal_defect_D(gamma, u)
        d1 = diagonal_defect_D(gamma, cyclic_tau(u))
        d_err = max(d_err, abs(d1 + d0))
    return CyclicEquivarianceAudit(
        G_equivariant=g_err < 1e-9,
        D_anti_equivariant=d_err < 1e-9,
        A_fourth_power_error=a4_err,
        det_A=float(np.linalg.det(CYCLIC_A)),
        max_G_error=g_err,
        max_D_anti_error=d_err,
    )


def G_preimage_tau_invariant(gamma: CurveFn, u: Sequence[float], tol: float = 1e-9) -> bool:
    """G(tau u)=0 iff G(u)=0 for every curve (exact linear relation on G-values)."""
    g0 = rhombus_map_G(gamma, u)
    g1 = rhombus_map_G(gamma, cyclic_tau(u))
    g0_zero = max(abs(x) for x in g0) <= tol
    g1_zero = max(abs(x) for x in g1) <= tol
    return g0_zero == g1_zero
