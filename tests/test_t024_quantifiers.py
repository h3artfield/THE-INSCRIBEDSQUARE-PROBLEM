"""Tests for T024 quantifier statements."""

import pytest

from squarepeg.residual_curves.primitive_obstruction import (
    log_tail_lower_bound,
    tail_interval_length,
)


@pytest.mark.fast
def test_shrinking_interval_length():
    m = 100.0
    assert tail_interval_length(m, m * m) < 0.25


@pytest.mark.fast
def test_area_lower_bound_uniform_in_m():
    assert log_tail_lower_bound(50.0, ratio=2.0) > log_tail_lower_bound(20.0, ratio=2.0)


@pytest.mark.fast
def test_obstruction_constant_positive():
    c0 = log_tail_lower_bound(1000.0, ratio=2.0)
    assert c0 > 0.5
