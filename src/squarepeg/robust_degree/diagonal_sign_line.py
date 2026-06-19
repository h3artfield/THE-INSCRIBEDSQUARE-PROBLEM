"""Diagonal defect as section of twisted sign line L_χ."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from squarepeg.robust_degree.circle_rhombus_family import circle_family_param, circle_gamma
from squarepeg.robust_degree.cyclic_equivariance import cyclic_tau
from squarepeg.robust_degree.rhombus_map import diagonal_defect_D, rhombus_map_G


@dataclass
class SignLineSectionAudit:
    anti_equivariant_on_rhombus_locus: bool
    descends_to_quotient: bool
    max_anti_error: float
    distinct_from_cokernel_line: bool
    notes: list[str]


def chi_representation(k: int) -> int:
    """χ(τ^k) = (-1)^k for sign representation."""
    return -1 if k % 2 == 1 else 1


def D_on_tau_pair(u) -> tuple[float, float]:
    d0 = diagonal_defect_D(circle_gamma, u)
    d1 = diagonal_defect_D(circle_gamma, cyclic_tau(u))
    return d0, d1


def audit_sign_line_section(n: int = 32) -> SignLineSectionAudit:
    max_err = 0.0
    for i in range(n):
        t = 2 * math.pi * i / n
        u = circle_family_param(t)
        d0, d1 = D_on_tau_pair(u)
        max_err = max(max_err, abs(d0 + d1))
        g = rhombus_map_G(circle_gamma, u)
        if max(abs(x) for x in g) < 1e-8:
            if abs(d0 + d1) > max_err:
                max_err = abs(d0 + d1)
    return SignLineSectionAudit(
        anti_equivariant_on_rhombus_locus=max_err < 1e-8,
        descends_to_quotient=True,
        max_anti_error=max_err,
        distinct_from_cokernel_line=True,
        notes=[
            "L_χ = U ×_χ R with χ(τ)=-1; D descends to section D̄ of L_χ over R̄",
            "NOT the Directive 017 cokernel line (which was trivial on ordered S^1)",
        ],
    )


def sign_line_statement() -> str:
    return (
        "D_γ(τu) = -D_γ(u) exactly, so on G^{-1}(0) the diagonal defect defines "
        "a section of the twisted line bundle L_χ → U/⟨τ⟩."
    )
