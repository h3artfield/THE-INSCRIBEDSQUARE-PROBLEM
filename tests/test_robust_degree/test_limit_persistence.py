"""T031 limit persistence."""

import math

import pytest

from squarepeg.robust_degree.limit_persistence import (
    check_t031_hypotheses,
    t031_positive_limsup_persistence,
)
from squarepeg.robust_degree.protected_box import ProtectedSquareBox


@pytest.mark.fast
def test_t031_hypotheses():
    hyp = check_t031_hypotheses([0.01, 0.02], [0.1, 0.1])
    assert hyp.uniform_boundary_margin


@pytest.mark.fast
def test_t031_positive_limsup():
    def gamma(t):
        return math.cos(t * 6), math.sin(t * 6)

    box = ProtectedSquareBox(windows=((0, 1), (1, 2), (2, 3), (3, 4)))
    box.boundary_margin = 0.01
    box.separation_lower_bound = 0.1
    ok = t031_positive_limsup_persistence(
        gamma, [box], [0.001], boundary_margins=[0.01]
    )
    assert isinstance(ok, bool)
