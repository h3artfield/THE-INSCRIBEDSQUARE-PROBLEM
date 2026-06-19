"""Tests for interval smooth curve evaluation."""

import pytest

from squarepeg.residual_curves.smooth_square_intervals import (
    F_interval,
    IVal,
    contains_zero,
    gamma_plus_interval,
)


@pytest.mark.fast
def test_gamma_plus_interval_contains_point():
    iv = IVal(6.5, 6.6)
    x_iv, y_iv = gamma_plus_interval(iv)
    from squarepeg.residual_curves.double_spiral import gamma_plus

    x, y = gamma_plus(6.55)
    assert x_iv.lo <= x <= x_iv.hi
    assert y_iv.lo <= y <= y_iv.hi


@pytest.mark.fast
def test_F_interval_contains_zero_at_root():
    from squarepeg.residual_curves.smooth_square_system import DISCOVERED_SMOOTH_THETA

    boxes = tuple(IVal(t - 0.15, t + 0.15) for t in DISCOVERED_SMOOTH_THETA)
    F_iv = F_interval(boxes)  # type: ignore[arg-type]
    assert all(contains_zero(iv) for iv in F_iv)
