"""Tests for T024 area obstruction."""

import pytest

from squarepeg.residual_curves.primitive_obstruction import (
    log_tail_lower_bound,
    relative_area_lower_bound,
    tail_obstructs_area_tightness,
)


@pytest.mark.fast
def test_log_tail_diverges():
    lb50 = log_tail_lower_bound(50.0, ratio=2.0)
    lb200 = log_tail_lower_bound(200.0, ratio=2.0)
    assert lb200 > lb50
    assert lb50 > 0.5


@pytest.mark.fast
def test_shrinking_interval_unbounded_area():
    cert = tail_obstructs_area_tightness(100.0, ratio=2.0)
    assert cert["param_interval_length"] < 0.25
    assert cert["tail_disk_radius"] < 0.15
    assert cert["area_lower_bound"] > 0.5
    assert cert["obstructs"]


@pytest.mark.fast
def test_relative_area_lower_bound_positive():
    assert relative_area_lower_bound(20.0, 400.0) > 0.3
