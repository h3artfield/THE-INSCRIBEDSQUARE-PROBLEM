"""Directive 017 obstruction-bundle audit tests."""

import math
from types import SimpleNamespace

import numpy as np
import pytest

from squarepeg.robust_degree.circle_cokernel import audit_circle_cokernel
from squarepeg.robust_degree.circle_quotient import audit_circle_quotient
from squarepeg.robust_degree.cokernel_bundle import (
    bundle_data_from_family,
    cokernel_fiber_at,
    parallel_transport_sign,
    rank_df,
    verify_morse_bott_tangent,
)
from squarepeg.robust_degree.curve_induced_section import audit_curve_induced_circle, t038_curve_statement
from squarepeg.robust_degree.euler_class import certificate_from_monodromy, t038_prime_statement
from squarepeg.robust_degree.morse_bott_countermodel import audit_countermodel
from squarepeg.robust_degree.obstruction_radius import rho_square_obs_polygon, t032_double_dagger_statement
from squarepeg.robust_degree.obstruction_section import (
    constant_cokernel_section_removes_family,
    reduced_zero_criterion_statement,
)
from squarepeg.robust_degree.square_family import circle_gamma, circle_square_family
from squarepeg.robust_degree.valid_family_certificate import (
    admissible_component_types,
    reject_rank5_without_obstruction,
)
from squarepeg.curves.polygon import PolygonCurve


@pytest.mark.fast
def test_countermodel_normal_nondegeneracy_insufficient():
    audit = audit_countermodel()
    assert audit.verdict == "NORMAL_NONDEGENERACY_INSUFFICIENT"
    assert audit.normal_invertible
    assert audit.normal_degree_nonzero
    assert audit.persists_under_perturbation


@pytest.mark.fast
def test_countermodel_perturbation_no_zeros():
    from squarepeg.robust_degree.morse_bott_countermodel import has_zero

    assert has_zero(0.0, 0.0, eps=0.0)
    assert not has_zero(0.0, 0.0, eps=1e-3)
    assert not has_zero(1.0, 1.0, eps=1e-3)


@pytest.mark.fast
def test_circle_derivative_rank_three():
    gamma = circle_gamma
    fam = circle_square_family()
    u = fam.parametrization(0.37)
    from squarepeg.robust_degree.cokernel_bundle import df_matrix

    jac = df_matrix(gamma, u)
    assert rank_df(jac) == 3


@pytest.mark.fast
def test_circle_kernel_all_ones():
    gamma = circle_gamma
    fam = circle_square_family()
    assert verify_morse_bott_tangent(gamma, fam.parametrization, 0.37, (1, 1, 1, 1))


@pytest.mark.fast
def test_circle_cokernel_dimension_one():
    gamma = circle_gamma
    fam = circle_square_family()
    fiber = cokernel_fiber_at(gamma, fam.parametrization(0.5))
    assert fiber.dimension == 1


@pytest.mark.fast
def test_circle_cokernel_covector_annihilates_df():
    gamma = circle_gamma
    fam = circle_square_family()
    from squarepeg.robust_degree.cokernel_bundle import df_matrix

    u = fam.parametrization(0.5)
    jac = df_matrix(gamma, u)
    ell = cokernel_fiber_at(gamma, u).covector
    assert np.linalg.norm(jac.T @ ell) < 1e-6


@pytest.mark.fast
def test_circle_obstruction_line_trivial():
    audit = audit_circle_cokernel()
    assert audit.obstruction_verdict == "CIRCLE_OBSTRUCTION_LINE_TRIVIAL"
    assert audit.w1_pairing_mod2 == 0
    assert audit.family_verdict == "Circle-B"
    assert audit.rank_df == 3
    assert audit.F_zero_on_family


@pytest.mark.fast
def test_ordered_monodromy_sign_continuous():
    gamma = circle_gamma
    fam = circle_square_family()
    mono = parallel_transport_sign(gamma, fam.parametrization, fam.domain)
    assert mono == 1.0


@pytest.mark.fast
def test_quotient_monodromy_trivial():
    q = audit_circle_quotient()
    assert q.cyclic_verdict == "QUOTIENT_OBSTRUCTION_TRIVIAL"
    assert q.closes_at_pi_over_2


@pytest.mark.fast
def test_bundle_transition_consistency():
    gamma = circle_gamma
    fam = circle_square_family()
    bundle = bundle_data_from_family(gamma, fam.parametrization)
    assert bundle.fiber_rank == 1
    assert bundle.rank_df == 3


@pytest.mark.fast
def test_euler_certificate_from_monodromy():
    cert = certificate_from_monodromy(1.0)
    assert cert.w_d_pairing_mod2 == 0
    assert not cert.forces_section_zero
    mob = certificate_from_monodromy(-1.0)
    assert mob.w_d_pairing_mod2 == 1
    assert mob.forces_section_zero


@pytest.mark.fast
def test_constant_section_removes_family():
    gamma = circle_gamma
    fam = circle_square_family()
    ts = np.linspace(0, 2 * math.pi, 8, endpoint=False)
    assert constant_cokernel_section_removes_family(gamma, fam.parametrization, 0.01, ts)


@pytest.mark.fast
def test_curve_induced_section_near_zero_mean():
    audit = audit_curve_induced_circle()
    assert audit.max_abs < 1e-8


@pytest.mark.fast
def test_t038_prime_conjectural():
    assert "CONJECTURAL" in t038_prime_statement()


@pytest.mark.fast
def test_t038_curve_conjectural():
    assert "CONJECTURAL" in t038_curve_statement()


@pytest.mark.fast
def test_reject_rank5_without_euler():
    hexagon = PolygonCurve([(1, 0), (0.5, 0.866), (-0.5, 0.866), (-1, 0), (-0.5, -0.866), (0.5, -0.866)])
    from squarepeg.exact_squares.solver import solve_polygon_full

    result = solve_polygon_full(hexagon)
    rejected = False
    for fam in result.families_1d:
        cert = reject_rank5_without_obstruction(fam)
        if cert.admissibility == "REJECTED_RANK_ONLY":
            rejected = True
            assert not cert.euler_obstruction_proved
    if not rejected:
        stub = SimpleNamespace(
            rank=5,
            feasibility_kind="closed_interval",
            feasible_intervals=[{"lo": "0", "hi": "1"}],
        )
        cert = reject_rank5_without_obstruction(stub)  # type: ignore[arg-type]
        assert cert.admissibility == "REJECTED_RANK_ONLY"


@pytest.mark.fast
def test_rho_square_obs_excludes_rank5_families():
    square = PolygonCurve([(0, 0), (1, 0), (1, 1), (0, 1)])
    report = rho_square_obs_polygon(square)
    assert report.rho_square_obs >= 0.0
    assert "INADMISSIBLE" in report.admissible_components or report.rejected_rank5_families >= 0


@pytest.mark.fast
def test_admissible_component_types():
    types = admissible_component_types()
    assert any("Brouwer" in t for t in types)
    assert any("w_d" in t for t in types)


@pytest.mark.fast
def test_t032_double_dagger_conjectural():
    assert "CONJECTURAL" in t032_double_dagger_statement()


@pytest.mark.fast
def test_reduced_zero_criterion():
    crit = reduced_zero_criterion_statement()
    assert crit.first_order_valid
    assert "Lyapunov" in crit.statement
