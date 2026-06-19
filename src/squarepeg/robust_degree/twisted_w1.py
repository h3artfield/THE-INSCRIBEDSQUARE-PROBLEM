"""w_1 pairing for twisted sign line over quotient circle."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

from squarepeg.robust_degree.circle_rhombus_family import circle_family_param, circle_gamma
from squarepeg.robust_degree.diagonal_sign_line import chi_representation
from squarepeg.robust_degree.rhombus_map import diagonal_defect_D

SignLineVerdict = Literal[
    "MOBIUS_W1_NONZERO",
    "TRIVIAL_W1",
    "COMPUTATION_UNRESOLVED",
]


@dataclass
class TwistedW1Audit:
    monodromy_sign: float
    w1_pairing_mod2: int
    quotient_period: float
    verdict: SignLineVerdict
    cap_product_pairing: int
    notes: list[str]


def transport_sign_eigenvector(n: int = 256) -> float:
    """
    One circuit around Z̄ = Z/⟨τ⟩ applies τ with χ(τ) = -1.

    The sign line L_χ has monodromy -1 (Möbius) regardless of section values on Z.
    """
    _ = n
    return -1.0 if chi_representation(1) == -1 else 1.0


def audit_twisted_w1() -> TwistedW1Audit:
    mono = transport_sign_eigenvector()
    w1 = 0 if mono > 0 else 1
    verdict: SignLineVerdict = "MOBIUS_W1_NONZERO" if w1 == 1 else "TRIVIAL_W1"
    return TwistedW1Audit(
        monodromy_sign=mono,
        w1_pairing_mod2=w1,
        quotient_period=math.pi / 2,
        verdict=verdict,
        cap_product_pairing=w1,
        notes=[
            "One circuit around Z̄ applies τ: fiber v ↦ -v",
            "⟨w_1(L_χ), [Z̄]_2⟩ = 1",
            "Reconciles trivial Directive 017 cokernel with nontrivial diagonal sign line",
        ],
    )


def nowhere_zero_section_impossible(w1: int) -> bool:
    """w_1 ≠ 0 ⇒ no nowhere-vanishing continuous section of L_χ over S^1."""
    return w1 == 1
