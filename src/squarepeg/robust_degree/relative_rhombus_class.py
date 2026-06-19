"""Relative Z_2 rhombus continuation class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.robust_degree.rhombus_continuation import (
    EG_perturbation_bound,
    certify_rhombus_continuation,
    normal_boundary_margin,
)

Framework = Literal["RELATIVE_SINGULAR_HOMOLOGY_Z2"]


@dataclass
class RelativeRhombusClass:
    """[R] in H_1(U, partial_nu U; Z_2) via mod-2 normal degree."""

    framework: Framework
    mod2_degree: int
    boundary_margin: float
    homotopy_invariant: bool
    definition: str


def relative_class_definition() -> str:
    return (
        "[R] = G^{-1}(0) cap U as mod-2 relative 1-cycle: class defined by the mod-2 "
        "degree of G restricted to each normal fiber {t} x D^3, paired with the fundamental "
        "class of (U, partial_nu U) in H_3(U, partial_nu U; Z_2)."
    )


def homotopy_invariance_lemma() -> str:
    return (
        "Homotopy Invariance (Z_2): If G_s : U -> R^3, s in [0,1], is a homotopy with "
        "G_s != 0 on partial_nu U for all s, then the relative mod-2 degree class [R_s] "
        "in H_1(U, partial_nu U; Z_2) is constant."
    )


def certify_relative_class(eta: float = 0.01) -> RelativeRhombusClass:
    cert = certify_rhombus_continuation(eta)
    return RelativeRhombusClass(
        framework="RELATIVE_SINGULAR_HOMOLOGY_Z2",
        mod2_degree=cert.mod2_normal_degree,
        boundary_margin=cert.normal_boundary_margin,
        homotopy_invariant=cert.boundary_zero_free,
        definition=relative_class_definition(),
    )


def perturbation_preserves_class(eta: float) -> bool:
    m_g = normal_boundary_margin()
    return EG_perturbation_bound(eta) < m_g
