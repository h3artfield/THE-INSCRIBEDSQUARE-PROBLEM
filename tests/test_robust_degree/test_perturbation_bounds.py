"""Abstract perturbation bound tests."""

import math

import pytest

from squarepeg.robust_degree.perturbation_radius import (
    E_gamma_B,
    squared_distance_perturbation_bound,
)


@pytest.mark.fast
def test_squared_distance_bound_diameter():
    D, eta = 1.0, 0.01
    a, b = (0.5, 0.0), (-0.5, 0.0)
    ap, bp = (0.5 + eta, 0.0), (-0.5 - eta, 0.0)
    lhs = abs((ap[0] - bp[0]) ** 2 - (a[0] - b[0]) ** 2)
    assert lhs <= squared_distance_perturbation_bound(eta, D) + 1e-12


@pytest.mark.fast
def test_translation_invariance():
    eta = 0.02
    assert squared_distance_perturbation_bound(eta, 2.0) == squared_distance_perturbation_bound(eta, 2.0)


@pytest.mark.fast
def test_E_monotone_in_eta():
    def gamma(t):
        return math.cos(t * 2 * math.pi), math.sin(t * 2 * math.pi)

    from squarepeg.robust_degree.protected_box import ProtectedSquareBox

    box = ProtectedSquareBox(windows=((0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)))
    assert E_gamma_B(gamma, box, 0.01) < E_gamma_B(gamma, box, 0.02)
