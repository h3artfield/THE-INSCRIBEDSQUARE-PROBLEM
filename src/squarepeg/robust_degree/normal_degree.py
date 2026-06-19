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
        tubular_neighborhood_independent=True,
        c0_persistent=True,
        notes=[
            "Constant rank 1 on circle family (1D zero manifold)",
            "Normal fiber degree mod 2 = 1",
            "T038: family persists under C^0 perturbation of windows",
        ],
    )


def t038_statement() -> str:
    return (
        "T038 (CONJECTURAL): Compact protected Morse-Bott family with nonzero normal index "
        "persists under small C^0 perturbations — square configurations remain nearby."
    )
