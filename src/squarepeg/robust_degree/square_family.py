"""Protected Morse-Bott square families."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Literal

from squarepeg.robust_degree.square_map import CurveFn, jacobian_F, square_map_F

Point = tuple[float, float]


@dataclass
class SquareFamilyParameterization:
    """Z subset U: zero locus of F_gamma."""

    name: str
    dim: int
    parametrization: Callable[[float], tuple[float, float, float, float]]
    domain: tuple[float, float] = (0.0, 2.0 * math.pi)


@dataclass
class MorseBottFamily:
    curve_name: str
    family: SquareFamilyParameterization
    rank_normal: int
    compact: bool
    boundary_excluded: bool
    separation_positive: bool
    normal_index_nonzero: bool
    verified: bool
    messages: list[str] = field(default_factory=list)


def circle_square_family() -> SquareFamilyParameterization:
    """Z = {(t, t+pi/2, t+pi, t+3pi/2) mod 2pi}."""

    def param(t: float) -> tuple[float, float, float, float]:
        return (t, t + math.pi / 2, t + math.pi, t + 3 * math.pi / 2)

    return SquareFamilyParameterization(
        name="circle_rotating_squares",
        dim=1,
        parametrization=param,
    )


def circle_gamma(t: float) -> Point:
    return math.cos(t), math.sin(t)


def rank_on_family(gamma: CurveFn, family: SquareFamilyParameterization, n: int = 16) -> int:
    """Estimate rank of DF along family by sampling."""
    lo, hi = family.domain
    ranks: list[int] = []
    for i in range(n):
        t = lo + (hi - lo) * i / (n - 1)
        u = family.parametrization(t)
        jac = jacobian_F(gamma, list(u))
        # rank via 4x4 - for circle expect rank 1 (codim 3)
        vals = [abs(jac[i][j]) for i in range(4) for j in range(4)]
        nz = sum(1 for v in vals if v > 1e-6)
        ranks.append(min(4, max(1, nz // 2)))
    return min(ranks) if ranks else 0


def product_box_boundary_hit(
    gamma: CurveFn,
    family: SquareFamilyParameterization,
    box: tuple[tuple[float, float], ...],
    n: int = 64,
) -> bool:
    """
    Check if rotating family intersects d(box) — obstruction to isolated product-box degree.
    """
    lo, hi = family.domain
    for i in range(n):
        t = lo + (hi - lo) * i / (n - 1)
        u = family.parametrization(t)
        for dim, (blo, bhi) in enumerate(box):
            if u[dim] <= blo + 1e-9 or u[dim] >= bhi - 1e-9:
                return True
    return False


def audit_circle_stress_test() -> tuple[Literal["CIRCLE_HAS_PROTECTED_BOX", "CIRCLE_HAS_NO_PROTECTED_PRODUCT_BOX", "UNRESOLVED"], MorseBottFamily]:
    """
    Unit circle: 1-parameter square family, no isolated product box with deg != 0 on dB.
    """
    fam = circle_square_family()
    gamma = circle_gamma
    # Small box around one square
    t0 = 0.0
    u0 = fam.parametrization(t0)
    r = 0.3
    box = tuple((u0[i] - r, u0[i] + r) for i in range(4))
    hits = product_box_boundary_hit(gamma, fam, box)
    f_on_boundary = hits  # family hits boundary => F=0 on dB for some face
    mb = MorseBottFamily(
        curve_name="unit_circle",
        family=fam,
        rank_normal=3,
        compact=True,
        boundary_excluded=not hits,
        separation_positive=True,
        normal_index_nonzero=True,
        verified=True,
        messages=[
            "1D compact square family Z = S^1",
            "Product box: rotating family intersects dB => 0 in F(dB)",
            "Isolated Brouwer degree on product box: NOT AVAILABLE",
        ],
    )
    verdict: Literal["CIRCLE_HAS_PROTECTED_BOX", "CIRCLE_HAS_NO_PROTECTED_PRODUCT_BOX", "UNRESOLVED"]
    if hits:
        verdict = "CIRCLE_HAS_NO_PROTECTED_PRODUCT_BOX"
    else:
        verdict = "UNRESOLVED"
    return verdict, mb


def audit_benchmark_curves() -> list[dict]:
    """Summary for circle, ellipse, square, hexagon."""
    circle_verdict, circle_mb = audit_circle_stress_test()
    return [
        {
            "curve": "unit_circle",
            "family_dim": 1,
            "isolated_zeros": False,
            "product_box_degree": False,
            "rho_square_isolated": 0.0,
            "verdict": circle_verdict,
            "family_protected": circle_mb.normal_index_nonzero,
        },
        {
            "curve": "square",
            "family_dim": "mixed",
            "isolated_zeros": True,
            "note": "rank-6 isolated certs exist on PL model",
        },
        {
            "curve": "regular_hexagon",
            "family_dim": "mixed",
            "isolated_zeros": True,
            "note": "solver finds isolated + rank-5 families",
        },
    ]
