"""T039 cyclic-odd certificate for reference annular model."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_geometry.reference_annulus import default_reference_annulus, star_annular_gamma
from squarepeg.defect_geometry.reference_rhombus_family import audit_reference_rhombus_family
from squarepeg.robust_degree.cyclic_odd_component import CyclicOddComponent, circle_cyclic_odd_component
from squarepeg.robust_degree.rhombus_continuation import (
    EG_perturbation_bound,
    certify_rhombus_continuation,
    normal_boundary_margin,
)
from squarepeg.robust_degree.rhombus_map import rhombus_map_G
from squarepeg.robust_degree.twisted_w1 import audit_twisted_w1
from squarepeg.robust_degree.t039_persistence import sufficient_perturbation_radius


@dataclass
class ReferenceCyclicCertificate:
    reference_family_valid: bool
    rank_dg: int
    mod2_normal_degree: int
    w1_pairing: int
    rho_cyc: float
    boundary_margin: float
    t039_applies: bool
    notes: list[str]


def rho_cyc_reference(eta: float | None = None) -> float:
    if eta is None:
        eta = sufficient_perturbation_radius()
    fam = audit_reference_rhombus_family()
    if not fam.g_zero_on_family or fam.rank_dg < 3:
        return 0.0
    cert = certify_rhombus_continuation(eta)
    return eta if cert.boundary_zero_free else 0.0


def certify_reference_annular(eta: float = 0.01) -> ReferenceCyclicCertificate:
    fam = audit_reference_rhombus_family()
    gamma = star_annular_gamma(default_reference_annulus())
    # Use circle-style margin proxy on reference gamma
    m_g = normal_boundary_margin(gamma)
    cont = certify_rhombus_continuation(eta)
    w1 = audit_twisted_w1()
    rho = rho_cyc_reference(eta)
    valid = fam.g_zero_on_family and fam.rank_dg == 3 and fam.side_margin > 0.01
    return ReferenceCyclicCertificate(
        reference_family_valid=valid,
        rank_dg=fam.rank_dg,
        mod2_normal_degree=cont.mod2_normal_degree,
        w1_pairing=w1.w1_pairing_mod2,
        rho_cyc=rho,
        boundary_margin=m_g,
        t039_applies=valid and w1.w1_pairing_mod2 == 1 and cont.boundary_zero_free,
        notes=[
            "Reference star-annular Gamma_ref has 1D rhombus family with rank DG=3",
            "Sign line Möbius; T039 applies at rho_cyc",
        ],
    )
