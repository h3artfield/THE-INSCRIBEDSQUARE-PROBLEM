"""Reference tower Jordan audit tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_geometry.reference_tower import (
    ReferenceTowerSpec,
    audit_reference_tower_jordan,
    finite_tower_gamma,
    level_radii,
)


@pytest.mark.fast
def test_finite_tower_gamma_samples():
    gamma = finite_tower_gamma(ReferenceTowerSpec(), depth=4)
    pts = [gamma(i / 64) for i in range(64)]
    assert len(pts) == 64
    assert all(abs(x) + abs(y) < 2 for x, y in pts)


@pytest.mark.fast
def test_jordan_audit_passes():
    audit = audit_reference_tower_jordan(depth=5)
    assert audit.is_simple_closed
    assert audit.all_levels_annular_certified
    assert audit.accumulation_is_unique


@pytest.mark.fast
def test_radii_geometric_decay():
    radii = level_radii(ReferenceTowerSpec(lambda_ratio=0.45), 5)
    assert radii[0] == 1.0
    assert radii[-1] < radii[0]
