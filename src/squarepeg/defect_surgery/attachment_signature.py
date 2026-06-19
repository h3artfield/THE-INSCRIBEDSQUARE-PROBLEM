"""Attachment signature moduli beta_n, sigma_n, chi_n (Directive 025)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_surgery.exact_component_decomposition import (
    CyclicDecomposition,
    PathComponent,
    master_area_identity,
)
from squarepeg.defect_surgery.concatenation_area import relative_area_path

Point = tuple[float, float]


@dataclass
class SignatureModuli:
    """Noncircular moduli on a parameter test interval J."""

    beta: float
    sigma: float
    chi: float
    alpha: float


def beta_retained_modulus(components: list[PathComponent]) -> float:
    """
    beta_n(J) = sum_{R in R_n(J)} |A_R|.

    Uses only retained subarcs — does not reference Q_n total area.
    """
    return sum(abs(c.intrinsic_area) for c in components if c.kind == "retained")


def sigma_attachment_modulus(components: list[PathComponent]) -> float:
    """
    sigma_n(J) = |A_{Z_{n,J}}| from component net displacements.

    Computed from attachment chain, not from alpha_{Q_n}.
    """
    ident = master_area_identity(components)
    return abs(ident.attachment_chain_area)


def chi_curved_modulus(components: list[PathComponent]) -> float:
    """chi_n(J) = sum_{C curved} |A_C|; zero for straight chords."""
    return sum(abs(c.intrinsic_area) for c in components if c.kind == "crosscut")


def alpha_from_moduli(beta: float, sigma: float, chi: float) -> float:
    """Exact upper bound from master identity."""
    return beta + sigma + chi


def moduli_from_decomposition(decomp: CyclicDecomposition) -> SignatureModuli:
    comps = decomp.components
    beta = beta_retained_modulus(comps)
    sigma = sigma_attachment_modulus(comps)
    chi = chi_curved_modulus(comps)
    ident = master_area_identity(comps)
    alpha = abs(ident.master_lhs)
    return SignatureModuli(beta=beta, sigma=sigma, chi=chi, alpha=alpha)


def verify_beta_noncircular(decomp: CyclicDecomposition, tol: float = 1e-9) -> bool:
    """beta uses only retained paths, never Q_n|_J total area."""
    manual = sum(
        abs(relative_area_path(c.path)) for c in decomp.components if c.kind == "retained"
    )
    return abs(manual - beta_retained_modulus(decomp.components)) <= tol


def verify_sigma_noncircular(decomp: CyclicDecomposition, tol: float = 1e-9) -> bool:
    """sigma uses attachment chain only."""
    from squarepeg.defect_surgery.exact_component_decomposition import (
        attachment_chain_area_from_deltas,
    )

    deltas = [c.delta for c in decomp.components]
    if not deltas:
        return True
    origin = decomp.components[0].path[0]
    a_z = abs(attachment_chain_area_from_deltas(origin, deltas))
    return abs(a_z - sigma_attachment_modulus(decomp.components)) <= tol


def alpha_bound_holds(decomp: CyclicDecomposition, tol: float = 1e-8) -> bool:
    """alpha_{Q_n}(J) <= beta + sigma + chi (exact equality for polygonal decomposition)."""
    m = moduli_from_decomposition(decomp)
    return m.alpha <= m.beta + m.sigma + m.chi + tol
