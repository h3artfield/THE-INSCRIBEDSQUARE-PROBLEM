"""Normalized defect blow-up scaling."""

import pytest

from squarepeg.robust_degree.recursive_defect import (
    absolute_vs_normalized_robustness,
    normalized_blow_up,
    recursive_spiral_comb_candidate,
)


@pytest.mark.fast
def test_absolute_radius_scales_with_r_k():
    assert absolute_vs_normalized_robustness(0.5, 0.01) == pytest.approx(0.005)


@pytest.mark.fast
def test_blow_up_notes():
    bu = normalized_blow_up([(0, 0), (0.1, 0), (0.1, 0.1)])
    assert any("O(r_k)" in n or "r_k" in n for n in bu.notes)


@pytest.mark.fast
def test_recursive_candidate_not_verified():
    c = recursive_spiral_comb_candidate()
    assert c.status == "CANDIDATE_NOT_VERIFIED"
