"""Cokernel bundle E = coker(DF|_Z) for Morse–Bott zero manifolds."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np

from squarepeg.robust_degree.square_map import CurveFn, jacobian_F

Param4 = tuple[float, float, float, float]
Parametrization = Callable[[float], Param4]


@dataclass
class CokernelFiber:
    """Fiber E_z = R^n / im(DF_z) at a point on Z."""

    dimension: int
    covector: np.ndarray  # unit vector in ker(DF^T) subset R^n


@dataclass
class CokernelBundleData:
    """Rank-d vector bundle data over a 1D parametrized zero manifold."""

    base_dim: int
    fiber_rank: int
    rank_df: int
    kernel_dim: int
    parametrization: Parametrization
    domain: tuple[float, float]
    regularity: str
    notes: list[str]


def df_matrix(
    gamma: CurveFn,
    u: Sequence[float],
    *,
    eps: float = 1e-7,
) -> np.ndarray:
    return np.array(jacobian_F(gamma, list(u), eps=eps), dtype=float)


def kernel_dimension(jac: np.ndarray, tol: float = 1e-5) -> int:
    s = np.linalg.svd(jac, compute_uv=False)
    return int(np.sum(s <= tol))


def rank_df(jac: np.ndarray, tol: float = 1e-5) -> int:
    return int(jac.shape[0] - kernel_dimension(jac, tol=tol))


def cokernel_covector(jac: np.ndarray, tol: float = 1e-8) -> np.ndarray:
    """Unit covector ell in ker(DF^T), i.e. left null vector of DF."""
    _, _, vh = np.linalg.svd(jac.T)
    ell = vh[-1].astype(float)
    n = np.linalg.norm(ell)
    if n < tol:
        raise ValueError("degenerate Jacobian: no cokernel direction")
    return ell / n


def cokernel_fiber_at(
    gamma: CurveFn,
    u: Sequence[float],
    *,
    eps: float = 1e-7,
) -> CokernelFiber:
    jac = df_matrix(gamma, u, eps=eps)
    rk = rank_df(jac)
    ker_dim = jac.shape[0] - rk
    ell = cokernel_covector(jac)
    return CokernelFiber(dimension=jac.shape[0] - rk, covector=ell)


def verify_morse_bott_tangent(
    gamma: CurveFn,
    parametrization: Parametrization,
    t: float,
    tangent: Sequence[float],
    *,
    eps: float = 1e-7,
    tol: float = 0.05,
) -> bool:
    """Check ker DF_z approximates span of dz/dt."""
    u = parametrization(t)
    jac = df_matrix(gamma, u, eps=eps)
    v = np.array(tangent, dtype=float)
    v = v / np.linalg.norm(v)
    s = np.linalg.svd(jac, compute_uv=False)
    # distance of v from row space: ||v - P v||
    u_mat, _, vh = np.linalg.svd(jac, full_matrices=True)
    # kernel of jac is right null space
    _, _, vh_r = np.linalg.svd(jac)
    ker = vh_r[-1]
    ker = ker / np.linalg.norm(ker)
    return abs(float(np.dot(v, ker)) - 1.0) <= tol or abs(float(np.dot(v, ker)) + 1.0) <= tol


def parallel_transport_sign(
    gamma: CurveFn,
    parametrization: Parametrization,
    domain: tuple[float, float],
    *,
    n_samples: int = 256,
    eps: float = 1e-7,
) -> float:
    """
    Transport cokernel line along Z with sign continuity.

    Returns +1 if monodromy is trivial, -1 if orientation flips once.
    """
    lo, hi = domain
    ts = np.linspace(lo, hi, n_samples, endpoint=False)
    ell = cokernel_fiber_at(gamma, parametrization(float(ts[0])), eps=eps).covector
    for t in ts[1:]:
        nxt = cokernel_fiber_at(gamma, parametrization(float(t)), eps=eps).covector
        if float(np.dot(ell, nxt)) < 0.0:
            nxt = -nxt
        ell = nxt
    start = cokernel_fiber_at(gamma, parametrization(float(ts[0])), eps=eps).covector
    end = ell
    dot = float(np.dot(start, end))
    if dot >= 0:
        return 1.0
    return -1.0


def bundle_data_from_family(
    gamma: CurveFn,
    parametrization: Parametrization,
    domain: tuple[float, float] = (0.0, 2.0 * math.pi),
) -> CokernelBundleData:
    t0 = 0.5 * (domain[0] + domain[1])
    u = parametrization(t0)
    jac = df_matrix(gamma, u)
    rk = rank_df(jac)
    ker_dim = jac.shape[0] - rk
    coker_dim = jac.shape[0] - rk
    return CokernelBundleData(
        base_dim=1,
        fiber_rank=coker_dim,
        rank_df=rk,
        kernel_dim=ker_dim,
        parametrization=parametrization,
        domain=domain,
        regularity="C^1 (gamma C^1, F C^1 on U)",
        notes=[
            "Fibers E_z = R^n / im(DF_z) assemble into rank-d bundle for Morse–Bott Z",
            "Transition functions continuous when DF has constant rank d on Z",
        ],
    )
