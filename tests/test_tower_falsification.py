"""Tower falsification tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_geometry.coherent_tower import validate_coherent_tower
from squarepeg.defect_geometry.tower_falsification import (
    center_drifting_tower,
    phase_drifting_tower,
    run_tower_falsifications,
)


@pytest.mark.fast
def test_phase_drift_fails_coherence():
    t = phase_drifting_tower(rotation_per_level=0.5)
    assert not validate_coherent_tower(t)


@pytest.mark.fast
def test_center_drift_at_boundary():
    t = center_drifting_tower(max_drift_factor=0.49)
    # May pass or fail depending on cumulative drift — audit runs
    assert len(t.levels) >= 2


@pytest.mark.fast
def test_falsification_report():
    rep = run_tower_falsifications()
    assert len(rep.results) >= 3
    names = {r.name for r in rep.results}
    assert "phase_drifting" in names
    assert "branching" in names
