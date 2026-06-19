"""Tower Theta bound tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_geometry.reference_tower import build_reference_tower
from squarepeg.defect_geometry.tower_reference_bound import (
    certified_tower_regime_nonempty,
    theta_tower_bound,
)


@pytest.mark.fast
def test_theta_includes_depth_sum():
    tower = build_reference_tower()
    b = theta_tower_bound(tower, depth=4)
    assert b.theta > b.components["per_level_psi"]
    assert b.depth_terms == 4


@pytest.mark.fast
def test_certified_tower_regime_empty():
    assert not certified_tower_regime_nonempty()


@pytest.mark.fast
def test_theta_exceeds_rho_tower():
    tower = build_reference_tower()
    b = theta_tower_bound(tower, depth=3)
    assert b.theta > b.rho_tower
    assert not b.sufficient
