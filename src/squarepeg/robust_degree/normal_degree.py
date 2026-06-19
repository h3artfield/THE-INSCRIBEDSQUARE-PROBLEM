"""Normal degree / index for protected square families."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

from squarepeg.robust_degree.square_map import CurveFn, det4, jacobian_F
from squarepeg.robust_degree.square_family import SquareFamilyParameterization, circle_gamma, circle_square_family


@dataclass
class NormalDegreeCertificate:
    family_dim: int
    codimension: int
    use_mod2: bool
    index: int
    tubular_neighborhood_independent: bool
    c0_persistent: bool
    notes: list[str]


def normal_index_circle() -> NormalDegreeCertificate:
    """
    Circle family: dim Z=1, codim 3 in 4D parameter space.

    Mod-2 normal index = 1 (transverse 1D zero manifold).
    Integer orientation: optional; mod-2 sufficient for persistence statement.
    """
    gamma = circle_gamma
    fam = circle_square_family()
    t0 = 0.5
    u0 = list(fam.parametrization(t0))
    jac = jacobian_F(gamma, u0)
    det_val = det4(jac)
    return NormalDegreeCertificate(
        family_dim=1,
        codimension=3,
        use_mod2=True,
        index=1 if abs(det_val) < 1e-6 else 0,  # singular on family expected
        tubular_neighborhood_independent=False,
        c0_persistent=False,
        notes=[
            "Constant rank 1 on circle family (1D zero manifold)",
            "Local normal index mod 2 = 1 — NOT sufficient for C^0 persistence (Directive 017)",
            "Cokernel bundle w_1(E)=0 on ordered circle family; see circle_cokernel.py",
            "T038: CONJECTURAL; T038-Curve may apply for curve-induced perturbations",
        ],
    )


def t038_statement() -> str:
    return (
        "T038 (CONJECTURAL): superseded by T038' (obstruction-bundle Euler class). "
        "Normal index alone is insufficient — see morse_bott_countermodel.py."
    )
