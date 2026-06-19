"""Exact LP certificate tests."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.dual_certificates import DualCertificate, no_positive_bound_certificate
from squarepeg.spectral_axioms.exact_verify import verify_grid_solution, verify_midpoint_objective
from squarepeg.spectral_axioms.grid_model import GridLPConfig, solve_grid_lp


@pytest.mark.fast
def test_kappa_one_dual_bound():
    cert = DualCertificate(
        kappa=Fraction(1),
        lower_bound=Fraction(1),
        description="g(x)=x from 1-Lipschitz with endpoints",
    )
    assert cert.lower_bound == Fraction(1)


@pytest.mark.fast
def test_exact_verification_all_kappa_sweep_values():
    for kappa in [Fraction(1), Fraction(11, 10), Fraction(2), Fraction(10)]:
        cfg = GridLPConfig(N=40, kappa=kappa, k=1)
        res = solve_grid_lp(cfg)
        assert res.status == "optimal"
        ok, errs = verify_grid_solution(res.values, cfg)
        assert ok, (kappa, errs)
        obj = verify_midpoint_objective(res.values, cfg)
        if kappa == Fraction(1):
            assert obj == Fraction(1)
        if kappa == Fraction(11, 10):
            assert obj == Fraction(0)


@pytest.mark.fast
def test_no_bound_certificate_for_large_kappa():
    cert = no_positive_bound_certificate(Fraction(2))
    assert cert.lower_bound == Fraction(0)
