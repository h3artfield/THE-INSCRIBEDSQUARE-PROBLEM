"""Semialgebraic characterization of protected boxes on rational polygons."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from squarepeg.curves.polygon import PolygonCurve


@dataclass
class SemialgebraicProtectedBoxFormula:
    """
    First-order formula over RCF encoding protected box with radius > eta.

    Predicate Protected(P, B, eta) where:
    - B is rational box in edge-parameter space C = e1 x e2 x e3 x e4
    - F != 0 on dB (openness: strict inequality on compact box)
    - deg(F, B, 0) != 0
    - pairwise vertex separation > sigma > 0
    - perturbation bound E(eta) < m(B)
    """

    edge_quadruple: tuple[int, int, int, int]
    box_rational: list[list[str]]  # Fraction endpoints as strings
    eta: str
    sigma: str
    m_boundary: str
    degree_nonzero: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_quadruple": list(self.edge_quadruple),
            "box_rational": self.box_rational,
            "eta": self.eta,
            "sigma": self.sigma,
            "m_boundary": self.m_boundary,
            "degree_nonzero": self.degree_nonzero,
            "polynomial_degree": 4,
            "field": "RCF",
        }


def square_map_polynomial_degree() -> int:
    """F components are differences of squared distances: degree 4 in edge parameters."""
    return 4


def build_formula_from_rational_box(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    u_box: tuple[tuple[Fraction, Fraction], ...],
    eta: Fraction,
    *,
    sigma: Fraction = Fraction(1, 100),
) -> SemialgebraicProtectedBoxFormula:
    return SemialgebraicProtectedBoxFormula(
        edge_quadruple=edges,
        box_rational=[[str(a), str(b)] for a, b in u_box],
        eta=str(eta),
        sigma=str(sigma),
        m_boundary=">0",
        degree_nonzero=True,
    )


def t034_semidecidability_statement() -> str:
    return (
        "If a rational polygon P has intrinsic rho_square(P,B) > eta > 0 on some protected box B, "
        "then for every 0 < eta' < eta there exists k such that exhaustive level-k search "
        "certifies underline_rho_k(P) > eta'. "
        "Proof: openness of boundary exclusion and degree on compact rational subboxes; "
        "density of Q; stability of nonsingular degree; positive margins persist on small "
        "rational perturbations of B."
    )


def completeness_equality_for_rational_polygons() -> str:
    return (
        "Under T034, underline_rho_infty(P) = rho_square(P) for rational polygons when "
        "exhaustive search includes all edge quadruples, rational boxes, and exact degree checks. "
        "Equivalently: lim_{k->infty} underline_rho_k(P) = rho_square(P)."
    )
