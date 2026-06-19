"""Tests: intrinsic vs certified robust radius."""

import pytest

from squarepeg.robust_degree.certified_lower_bound import (
    monotonicity_underline_rho,
    never_return_zero_without_proof,
    underline_rho_infinity,
)
from squarepeg.robust_degree.intrinsic_radius import (
    intrinsic_positive_iff_c0_protected,
    intrinsic_rho_box,
)


@pytest.mark.fast
def test_certified_leq_intrinsic_in_principle():
    """underline_rho_k is a lower bound; may be strictly less than intrinsic rho."""
    assert never_return_zero_without_proof("NOT_FOUND_AT_LEVEL_K")


@pytest.mark.fast
def test_monotone_underline_rho():
    assert monotonicity_underline_rho([0.0, 0.001, 0.002, 0.002])


@pytest.mark.fast
def test_underline_rho_infty():
    assert underline_rho_infinity([0.0, 0.01, 0.005]) == 0.01


@pytest.mark.fast
def test_intrinsic_positive_iff_protected():
    import math

    def gamma(t):
        return math.cos(t * 6), math.sin(t * 6)

    from squarepeg.robust_degree.protected_box import ProtectedSquareBox

    box = ProtectedSquareBox(windows=((0, 1), (1, 2), (2, 3), (3, 4)))
    r = intrinsic_rho_box(gamma, box, boundary_margin=0.01, separation_margin=0.1)
    assert intrinsic_positive_iff_c0_protected(gamma, r) == (r > 0)
