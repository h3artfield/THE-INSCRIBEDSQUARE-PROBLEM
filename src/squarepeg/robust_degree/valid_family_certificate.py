"""Valid protected square family certificate with Euler obstruction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.families import AffineSquareFamily1D
from squarepeg.robust_degree.family_certificate import classify_rank5_family

Admissibility = Literal[
    "ADMISSIBLE_ISOLATED_DEGREE",
    "ADMISSIBLE_OBSTRUCTION_BUNDLE",
    "ADMISSIBLE_CURVE_RESTRICTED",
    "REJECTED_RANK_ONLY",
    "REJECTED_NO_BOUNDARY_EXCLUSION",
    "REJECTED_TRIVIAL_OBSTRUCTION",
    "UNSUPPORTED",
]


@dataclass
class ProtectedSquareFamilyCertificateV2:
    """Certificate requiring proved continuation obstruction, not rank alone."""

    family: AffineSquareFamily1D | None
    name: str
    zero_dim: int
    cokernel_rank: int
    compact: bool
    boundary_excluded: bool
    collision_margin_positive: bool
    w_d_pairing_mod2: int | None
    euler_obstruction_proved: bool
    admissibility: Admissibility
    messages: list[str] = field(default_factory=list)


def reject_rank5_without_obstruction(fam: AffineSquareFamily1D) -> ProtectedSquareFamilyCertificateV2:
    kind = classify_rank5_family(fam)
    if kind != "genuine_1d_family":
        return ProtectedSquareFamilyCertificateV2(
            family=fam,
            name=fam.description if hasattr(fam, "description") else "rank5",
            zero_dim=0,
            cokernel_rank=0,
            compact=False,
            boundary_excluded=False,
            collision_margin_positive=False,
            w_d_pairing_mod2=None,
            euler_obstruction_proved=False,
            admissibility="UNSUPPORTED",
            messages=[f"family kind {kind} — not a genuine 1D component"],
        )
    return ProtectedSquareFamilyCertificateV2(
        family=fam,
        name="rank5_family",
        zero_dim=1,
        cokernel_rank=3,
        compact=fam.feasibility_kind in ("closed_interval", "union", "point"),
        boundary_excluded=False,
        collision_margin_positive=True,
        w_d_pairing_mod2=None,
        euler_obstruction_proved=False,
        admissibility="REJECTED_RANK_ONLY",
        messages=[
            "Rank-5 nullity alone does NOT certify protected family",
            "Requires w_d(E) pairing or curve-restricted obstruction theorem",
            "Directive 017: do not issue certificate from rank only",
        ],
    )


def admissible_component_types() -> list[str]:
    return [
        "isolated components with nonzero Brouwer degree",
        "Morse-Bott components with nonzero w_d(E) pairing",
        "curve-restricted components with proved T038-Curve",
    ]
