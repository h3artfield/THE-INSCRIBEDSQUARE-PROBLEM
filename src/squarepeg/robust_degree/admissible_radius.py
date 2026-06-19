"""Admissible obstruction-protected radius rho_square^adm."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.robust_degree.obstruction_radius import rho_square_obs_polygon
from squarepeg.robust_degree.cyclic_odd_component import circle_cyclic_odd_component
from squarepeg.robust_degree.t039_persistence import sufficient_perturbation_radius
from squarepeg.robust_degree.valid_family_certificate import reject_rank5_without_obstruction

ComponentClass = Literal[
    "ISOLATED_BROUWER",
    "EULER_OBSTRUCTION",
    "CYCLIC_ODD_RHOMBUS",
    "CURVE_RESTRICTED",
    "INADMISSIBLE",
]

FamilyAuditStatus = Literal[
    "CYCLIC_ODD_CERTIFIED",
    "EULER_OBSTRUCTION_CERTIFIED",
    "UNPROTECTED_FAMILY",
    "ASSIGNMENT_ARTIFACT",
    "UNRESOLVED",
]


@dataclass
class AdmissibleRadiusReport:
    rho_square_adm: float
    isolated_contribution: float
    cyclic_odd_contribution: float
    admissible_components: list[ComponentClass]
    rejected_families: int
    messages: list[str] = field(default_factory=list)


def rho_square_cyc(component_name: str = "unit_circle", eta: float | None = None) -> float:
    """Certified C^0 radius for cyclic-odd component (curve-level)."""
    if eta is None:
        eta = sufficient_perturbation_radius()
    comp = circle_cyclic_odd_component(eta)
    return eta if comp.certified else 0.0


def rho_square_adm_polygon(
    polygon: PolygonCurve,
    *,
    param_radius: float = 0.05,
) -> AdmissibleRadiusReport:
    obs = rho_square_obs_polygon(polygon, param_radius=param_radius)
    cyclic = 0.0
    msgs = list(obs.messages)
    # Circle cyclic-odd certificate applies to curves, not finite polygons directly
    rejected = obs.rejected_rank5_families
    admissible: list[ComponentClass] = []
    for c in obs.admissible_components:
        if c == "ISOLATED_BROUWER":
            admissible.append("ISOLATED_BROUWER")
        elif c == "INADMISSIBLE":
            admissible.append("INADMISSIBLE")
    return AdmissibleRadiusReport(
        rho_square_adm=obs.rho_square_obs + cyclic,
        isolated_contribution=obs.isolated_contribution,
        cyclic_odd_contribution=cyclic,
        admissible_components=admissible,
        rejected_families=rejected,
        messages=msgs,
    )


def audit_rank5_family_status(fam) -> FamilyAuditStatus:
    cert = reject_rank5_without_obstruction(fam)
    if cert.admissibility == "REJECTED_RANK_ONLY":
        return "UNPROTECTED_FAMILY"
    if cert.admissibility == "UNSUPPORTED":
        return "ASSIGNMENT_ARTIFACT"
    return "UNRESOLVED"


def rho_square_adm_definition() -> str:
    return (
        "rho_square^adm(gamma) = sup certified persistence radii over: "
        "isolated Brouwer, Euler obstruction Morse-Bott, cyclic-odd rhombus components."
    )


def t032_section_statement() -> str:
    return (
        "T032§ (CONJECTURAL_FULL_BRIDGE): Admissible-protected component radii →0 "
        "⇒ area-tight subsequence. T038-Curve clean-room verified; not attacked here."
    )


def admissible_component_policy() -> str:
    return (
        "rho_square^adm includes: (1) isolated Brouwer degree, (2) proved Euler obstruction, "
        "(3) proved cyclic-odd T039 components. Excludes T038-prime without full proof."
    )
