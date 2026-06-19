"""Circle square-family cokernel bundle audit."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

from squarepeg.robust_degree.cokernel_bundle import (
    bundle_data_from_family,
    cokernel_fiber_at,
    df_matrix,
    parallel_transport_sign,
    rank_df,
    verify_morse_bott_tangent,
)
from squarepeg.robust_degree.euler_class import certificate_from_monodromy
from squarepeg.robust_degree.square_family import circle_gamma, circle_square_family
from squarepeg.robust_degree.square_map import square_map_F

CircleObstructionVerdict = Literal[
    "CIRCLE_OBSTRUCTION_LINE_TRIVIAL",
    "CIRCLE_OBSTRUCTION_LINE_NONTRIVIAL",
    "COMPUTATION_UNRESOLVED",
]

CircleFamilyVerdict = Literal[
    "Circle-A",
    "Circle-B",
    "Circle-C",
    "Circle-D",
]


@dataclass
class CircleCokernelAudit:
    rank_df: int
    kernel_spanned_by_all_ones: bool
    cokernel_dim: int
    covector_at_sample: list[float]
    monodromy_sign: float
    w1_pairing_mod2: int
    obstruction_verdict: CircleObstructionVerdict
    family_verdict: CircleFamilyVerdict
    F_zero_on_family: bool
    notes: list[str]


def explicit_cokernel_covector(t: float) -> np.ndarray:
    gamma = circle_gamma
    fam = circle_square_family()
    u = fam.parametrization(t)
    return cokernel_fiber_at(gamma, u).covector


def audit_circle_cokernel(n_samples: int = 256) -> CircleCokernelAudit:
    gamma = circle_gamma
    fam = circle_square_family()
    bundle = bundle_data_from_family(gamma, fam.parametrization, fam.domain)

    t_sample = 0.37
    u = fam.parametrization(t_sample)
    jac = df_matrix(gamma, u)
    rk = rank_df(jac)
    ker_ok = verify_morse_bott_tangent(gamma, fam.parametrization, t_sample, (1.0, 1.0, 1.0, 1.0))

    # F = 0 on family
    f_max = 0.0
    for i in range(16):
        t = fam.domain[0] + (fam.domain[1] - fam.domain[0]) * i / 15
        F = square_map_F(gamma, fam.parametrization(t))
        f_max = max(f_max, max(abs(x) for x in F))

    mono = parallel_transport_sign(gamma, fam.parametrization, fam.domain, n_samples=n_samples)
    euler = certificate_from_monodromy(mono, bundle_rank=1, base_dim=1)

    if euler.w_d_pairing_mod2 == 0:
        obs: CircleObstructionVerdict = "CIRCLE_OBSTRUCTION_LINE_TRIVIAL"
        family: CircleFamilyVerdict = "Circle-B"
    elif euler.w_d_pairing_mod2 == 1:
        obs = "CIRCLE_OBSTRUCTION_LINE_NONTRIVIAL"
        family = "Circle-A"
    else:
        obs = "COMPUTATION_UNRESOLVED"
        family = "Circle-D"

    ell = cokernel_fiber_at(gamma, u).covector
    return CircleCokernelAudit(
        rank_df=rk,
        kernel_spanned_by_all_ones=ker_ok,
        cokernel_dim=4 - rk,
        covector_at_sample=ell.tolist(),
        monodromy_sign=mono,
        w1_pairing_mod2=euler.w_d_pairing_mod2,
        obstruction_verdict=obs,
        family_verdict=family,
        F_zero_on_family=f_max < 1e-8,
        notes=[
            "Ordered family Z = {(t, t+pi/2, t+pi, t+3pi/2) : t in R/2piZ}",
            "rank DF = 3, ker DF = span(1,1,1,1) = T_z Z",
            "Local normal index = 1 does NOT determine w_1(E); monodromy computed by parallel transport",
            "Trivial line bundle => constant cokernel section can remove abstract family",
        ],
    )
