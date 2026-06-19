"""Annular forest bridge tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.annular_forest_bridge import audit_annular_surgery_forest
from squarepeg.defect_surgery.fat_disk_packing import packing_estimate_sum_diam_sq
from squarepeg.defect_surgery.examples import example_bump_disk


@pytest.mark.fast
def test_annular_forest_audit():
    audit = audit_annular_surgery_forest()
    assert audit.annular_isolated or audit.fat_disks


@pytest.mark.fast
def test_fat_packing():
    p = packing_estimate_sum_diam_sq([example_bump_disk()], (1.5, 0.0), R=2.0)
    assert p.satisfied
