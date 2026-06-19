"""Coherent tower tests (Directive 022)."""

from __future__ import annotations

import pytest

from squarepeg.defect_geometry.coherent_tower import (
    TowerConstants,
    validate_coherent_tower,
)
from squarepeg.defect_geometry.reference_tower import build_reference_tower


@pytest.mark.fast
def test_reference_tower_coherent():
    tower = build_reference_tower()
    assert validate_coherent_tower(tower)
    assert tower.levels[0].outer_radius == 1.0
    assert 0.42 <= tower.levels[1].outer_radius / tower.levels[0].outer_radius <= 0.48


@pytest.mark.fast
def test_scale_decay():
    tower = build_reference_tower()
    c = tower.constants
    for j in range(len(tower.levels) - 1):
        ratio = tower.levels[j + 1].outer_radius / tower.levels[j].outer_radius
        assert c.lambda_minus <= ratio <= c.lambda_plus
