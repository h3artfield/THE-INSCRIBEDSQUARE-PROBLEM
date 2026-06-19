"""Tests for smooth truncation convergence."""

import pytest

from squarepeg.residual_curves.smooth_truncations import smooth_tail_cutoff


@pytest.mark.fast
def test_cutoff_is_one_before_cut():
    assert smooth_tail_cutoff(5.0, 10.0) == 1.0


@pytest.mark.fast
def test_cutoff_is_zero_far_out():
    assert smooth_tail_cutoff(20.0, 10.0) == 0.0
