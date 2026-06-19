"""Directive 018 cyclic-odd rhombus continuation tests."""

import math

import numpy as np
import pytest

from squarepeg.robust_degree.admissible_radius import audit_rank5_family_status, rho_square_adm_polygon
from squarepeg.robust_degree.circle_rhombus_family import (
    EXPECTED_DF_CIRCLE,
    audit_circle_rhombus_family,
    circle_family_param,
    circle_gamma,
    first_order_diagonal_variation,
    verify_anti_periodicity_delta,
)
from squarepeg.robust_degree.continuous_curve_limit import audit_continuous_passage
from squarepeg.robust_degree.cyclic_equivariance import (
    CYCLIC_A,
    audit_cyclic_equivariance,
    cyclic_tau,
    verify_A_properties,
)
from squarepeg.robust_degree.cyclic_odd_persistence import audit_cyclic_odd_persistence, t038_curve_statement
from squarepeg.robust_degree.diagonal_sign_line import audit_sign_line_section
from squarepeg.robust_degree.rhombus_continuation import certify_rhombus_continuation, normal_boundary_margin
from squarepeg.robust_degree.rhombus_map import (
    diagonal_defect_D,
    is_square_configuration,
    rhombus_map_G,
    square_map_from_parts,
)
from squarepeg.robust_degree.square_map import jacobian_F, square_map_F
from squarepeg.robust_degree.twisted_w1 import audit_twisted_w1, nowhere_zero_section_impossible
from squarepeg.curves.polygon import PolygonCurve
from types import SimpleNamespace


@pytest.mark.fast
def test_cyclic_A_fourth_power():
    ok, det_ok, err = verify_A_properties()
    assert ok
    assert det_ok
    assert err < 1e-12


@pytest.mark.fast
def test_cyclic_A_det_minus_one():
    assert abs(float(np.linalg.det(CYCLIC_A)) + 1.0) < 1e-12


@pytest.mark.fast
def test_D_anti_under_tau():
    u = circle_family_param(0.3)
    d0 = diagonal_defect_D(circle_gamma, u)
    d1 = diagonal_defect_D(circle_gamma, cyclic_tau(u))
    assert abs(d0 + d1) < 1e-10


@pytest.mark.fast
def test_G_equivariant_under_tau():
    samples = [circle_family_param(t) for t in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
    audit = audit_cyclic_equivariance(circle_gamma, samples)
    assert audit.G_equivariant
    assert audit.D_anti_equivariant


@pytest.mark.fast
def test_F_equals_rhombus_plus_diagonal():
    u = circle_family_param(0.5)
    f_parts = square_map_from_parts(circle_gamma, u)
    f_orig = tuple(square_map_F(circle_gamma, u))
    assert all(abs(a - b) < 1e-12 for a, b in zip(f_parts, f_orig))


@pytest.mark.fast
def test_circle_df_matches_expected():
    audit = audit_circle_rhombus_family()
    assert audit.rank_DF == 3
    assert audit.rank_DG == 3
    assert audit.df_matches_expected
    assert audit.kernel_equals_tangent
    assert audit.G_zero_on_family
    assert audit.D_zero_on_family


@pytest.mark.fast
def test_circle_rhombus_jacobian_explicit():
    u = circle_family_param(0.37)
    df = np.array(jacobian_F(circle_gamma, u))
    assert np.max(np.abs(df - EXPECTED_DF_CIRCLE)) < 1e-5


@pytest.mark.fast
def test_first_order_diagonal_anti_periodic():
    def h(t: float) -> tuple[float, float]:
        return (0.1 * math.sin(2 * t), 0.05 * math.cos(3 * t))

    assert verify_anti_periodicity_delta(h, 0.4)


@pytest.mark.fast
def test_first_order_formula_numeric():
    def h(t: float) -> tuple[float, float]:
        return (0.1 * math.sin(2 * t), 0.0)

    t = 0.4
    z = circle_family_param(t)
    eps = 1e-5
    d0 = diagonal_defect_D(circle_gamma, z)

    def ge(tt: float) -> tuple[float, float]:
        x, y = circle_gamma(tt)
        hx, hy = h(tt)
        return x + eps * hx, y + eps * hy

    d1 = diagonal_defect_D(ge, z)
    numeric = (d1 - d0) / eps
    formula = first_order_diagonal_variation(h, t)
    assert abs(numeric - formula) < 1e-3


@pytest.mark.fast
def test_rhombus_boundary_margin_positive():
    assert normal_boundary_margin() > 0.1


@pytest.mark.fast
def test_rhombus_continuation_eta():
    cert = certify_rhombus_continuation(0.01)
    assert cert.mod2_normal_degree == 1
    assert cert.boundary_zero_free


@pytest.mark.fast
def test_sign_line_mobius():
    w1 = audit_twisted_w1()
    assert w1.verdict == "MOBIUS_W1_NONZERO"
    assert w1.w1_pairing_mod2 == 1
    assert nowhere_zero_section_impossible(w1.w1_pairing_mod2)


@pytest.mark.fast
def test_sign_line_distinct_from_cokernel():
    sign = audit_sign_line_section()
    assert sign.distinct_from_cokernel_line


@pytest.mark.fast
def test_square_from_rhombus_and_diagonal():
    u = circle_family_param(0.0)
    assert is_square_configuration(circle_gamma, u)


@pytest.mark.fast
def test_cyclic_odd_persistence_outcome():
    audit = audit_cyclic_odd_persistence(0.01)
    assert audit.rhombus_continuation_valid
    assert audit.w1_pairing_nonzero
    assert audit.diagonal_must_vanish
    assert audit.outcome == "T038_CURVE_PROVED"


@pytest.mark.fast
def test_t038_curve_proved_locally():
    assert "PROVED_LOCALLY" in t038_curve_statement()


@pytest.mark.fast
def test_continuous_limit_audit():
    audit = audit_continuous_passage()
    assert audit.smooth_stage_valid
    assert audit.uniform_limit_valid


@pytest.mark.fast
def test_rank5_not_cyclic_odd_certified():
    stub = SimpleNamespace(rank=5, feasibility_kind="closed_interval", feasible_intervals=[{}])
    assert audit_rank5_family_status(stub) == "UNPROTECTED_FAMILY"  # type: ignore[arg-type]


@pytest.mark.fast
def test_rho_square_adm_polygon():
    square = PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])
    report = rho_square_adm_polygon(square)
    assert report.rho_square_adm >= 0.0
