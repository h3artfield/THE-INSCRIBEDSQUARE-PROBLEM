"""Quotient configuration space obstruction audit (cyclic / dihedral)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

from squarepeg.robust_degree.cokernel_bundle import cokernel_fiber_at, parallel_transport_sign
from squarepeg.robust_degree.euler_class import certificate_from_monodromy
from squarepeg.robust_degree.square_family import circle_gamma, circle_square_family

QuotientVerdict = Literal[
    "QUOTIENT_OBSTRUCTION_TRIVIAL",
    "QUOTIENT_OBSTRUCTION_NONTRIVIAL",
    "QUOTIENT_COMPUTATION_UNRESOLVED",
]


@dataclass
class QuotientObstructionAudit:
    cyclic_period: float
    ordered_monodromy: float
    cyclic_monodromy: float
    dihedral_note: str
    cyclic_verdict: QuotientVerdict
    closes_at_pi_over_2: bool
    notes: list[str]


def cyclic_param(t: float) -> tuple[float, float, float, float]:
    """Same ordered parametrization; domain quotient is pi/2."""
    fam = circle_square_family()
    return fam.parametrization(t)


def audit_circle_quotient() -> QuotientObstructionAudit:
    gamma = circle_gamma
    fam = circle_square_family()
    period = math.pi / 2

    ordered_mono = parallel_transport_sign(gamma, fam.parametrization, (0.0, 2.0 * math.pi))
    cyclic_mono = parallel_transport_sign(gamma, cyclic_param, (0.0, period))

    ordered_cert = certificate_from_monodromy(ordered_mono)
    cyclic_cert = certificate_from_monodromy(cyclic_mono)

    if cyclic_cert.w_d_pairing_mod2 == 1:
        cyclic_verdict: QuotientVerdict = "QUOTIENT_OBSTRUCTION_NONTRIVIAL"
    elif cyclic_cert.w_d_pairing_mod2 == 0:
        cyclic_verdict = "QUOTIENT_OBSTRUCTION_TRIVIAL"
    else:
        cyclic_verdict = "QUOTIENT_COMPUTATION_UNRESOLVED"

    # Check physical square repeats at pi/2 (cyclic relabel)
    u0 = fam.parametrization(0.0)
    u1 = fam.parametrization(period)
    closes = all(abs((b - a) - period) < 1e-9 for a, b in zip(u0, u1))

    return QuotientObstructionAudit(
        cyclic_period=period,
        ordered_monodromy=ordered_mono,
        cyclic_monodromy=cyclic_mono,
        dihedral_note="Dihedral relabeling flips orientation on two coordinates; not required for w_1 on circle family",
        cyclic_verdict=cyclic_verdict,
        closes_at_pi_over_2=closes,
        notes=[
            "Ordered space: period 2pi in t",
            "Cyclic quotient identifies t ~ t + pi/2 (vertex relabeling)",
            "Both ordered and cyclic quotients yield trivial w_1 for circle",
            "Persistence theorem must use space where obstruction class is genuinely nonzero",
        ],
    )
