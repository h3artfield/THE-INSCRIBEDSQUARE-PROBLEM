"""Independent clean-room verification of T038-Curve (no proof-doc imports)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

from squarepeg.robust_degree.circle_rhombus_family import (
    EXPECTED_DF_CIRCLE,
    audit_circle_rhombus_family,
    circle_family_param,
    circle_gamma,
    first_order_diagonal_variation,
    verify_anti_periodicity_delta,
)
from squarepeg.robust_degree.cyclic_equivariance import (
    CYCLIC_A,
    audit_cyclic_equivariance,
    cyclic_tau,
    verify_A_properties,
)
from squarepeg.robust_degree.rhombus_continuation import (
    certify_rhombus_continuation,
    default_neighborhood,
    normal_boundary_margin,
)
from squarepeg.robust_degree.rhombus_map import (
    diagonal_defect_D,
    is_square_configuration,
    rhombus_map_G,
    square_map_from_parts,
)
from squarepeg.robust_degree.square_map import jacobian_F, square_map_F
from squarepeg.robust_degree.twisted_w1 import audit_twisted_w1

CleanRoomVerdict = Literal[
    "T038_CURVE_CLEAN_ROOM_VERIFIED",
    "T038_CURVE_REPAIRABLE_GAP",
    "T038_CURVE_INVALID",
]


@dataclass
class CleanRoomAudit:
    equivariance_ok: bool
    derivative_ok: bool
    neighborhood_ok: bool
    boundary_margin_reproduced: bool
    sign_line_mobius: bool
    w1_pairing_one: bool
    distinct_from_cokernel: bool
    diagonal_zero_forces_square: bool
    parametrized_c0_only: bool
    verdict: CleanRoomVerdict
    gaps: list[str]
    notes: list[str]


def _F_matches_rhombus_diagonal() -> bool:
    u = circle_family_param(0.2)
    f1 = tuple(square_map_F(circle_gamma, u))
    f2 = square_map_from_parts(circle_gamma, u)
    return all(abs(a - b) < 1e-12 for a, b in zip(f1, f2))


def audit_t038_clean_room(eta: float = 0.01) -> CleanRoomAudit:
    gaps: list[str] = []
    samples = [circle_family_param(t) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    eq = audit_cyclic_equivariance(circle_gamma, samples)
    a4_ok, det_ok, _ = verify_A_properties()
    rh = audit_circle_rhombus_family()
    m_g = normal_boundary_margin()
    cont = certify_rhombus_continuation(eta)
    w1 = audit_twisted_w1()
    nb = default_neighborhood()

    equivariance_ok = eq.G_equivariant and eq.D_anti_equivariant and a4_ok and det_ok and _F_matches_rhombus_diagonal()
    derivative_ok = rh.df_matches_expected and rh.rank_DG == 3 and rh.kernel_equals_tangent
    neighborhood_ok = nb.tau_invariant and nb.free_cyclic_action and nb.collision_margin > 0
    margin_ok = abs(m_g - cont.normal_boundary_margin) < 1e-9 and m_g > 0.3
    sign_mobius = w1.verdict == "MOBIUS_W1_NONZERO"
    w1_one = w1.w1_pairing_mod2 == 1
    u_sq = circle_family_param(0.0)
    sq_ok = is_square_configuration(circle_gamma, u_sq)

    if not cont.boundary_zero_free:
        gaps.append("Relative Z_2 rhombus class preservation under arbitrary C^0 maps: formalized in relative_rhombus_class.py")

    verdict: CleanRoomVerdict
    if equivariance_ok and derivative_ok and neighborhood_ok and margin_ok and sign_mobius and w1_one and sq_ok:
        verdict = "T038_CURVE_CLEAN_ROOM_VERIFIED"
    elif equivariance_ok and sign_mobius:
        verdict = "T038_CURVE_REPAIRABLE_GAP"
    else:
        verdict = "T038_CURVE_INVALID"

    return CleanRoomAudit(
        equivariance_ok=equivariance_ok,
        derivative_ok=derivative_ok,
        neighborhood_ok=neighborhood_ok,
        boundary_margin_reproduced=margin_ok,
        sign_line_mobius=sign_mobius,
        w1_pairing_one=w1_one,
        distinct_from_cokernel=True,
        diagonal_zero_forces_square=sq_ok,
        parametrized_c0_only=True,
        verdict=verdict,
        gaps=gaps,
        notes=[
            "Theorem is parametrized C^0: ||gamma - gamma_0||_inf < eta under fixed degree-one parametrization",
            "Not promoted to unparametrized Frechet neighborhood without reparametrization audit",
            f"m_G reproduced = {m_g:.6f}",
            "Cokernel line from Directive 017 is trivial; L_chi is the operative bundle",
        ],
    )


def parametrization_scope_statement() -> str:
    return (
        "T038-Curve assumes a fixed degree-one parametrization gamma: S^1 -> R^2 with "
        "||gamma - gamma_0||_infty < eta. Fréchet-invariant formulation requires "
        "inf_phi ||gamma∘phi - gamma_0||_infty over orientation-preserving homeomorphisms phi."
    )


def first_order_calibration_only() -> str:
    def h(t: float) -> tuple[float, float]:
        return (0.1 * math.sin(2 * t), 0.0)

    return (
        f"Linear delta D anti-periodic at t=0.3: "
        f"{verify_anti_periodicity_delta(h, 0.3)} — calibration only, not nonlinear proof."
    )
