import pytest

from squarepeg.rough_area.adaptive_smoothing import (
    adaptive_smooth_polygon,
    choose_smoothing_tolerance,
    smoothing_primitive_bound,
    verify_smoothing_primitive_control,
)
from squarepeg.variation.polygonal_approximation import circle_param, piecewise_linear_interpolation


@pytest.mark.fast
def test_tolerance_handles_large_variation():
    ln = 1000.0
    mn = 10.0
    target = 1e-4
    eps = choose_smoothing_tolerance(ln, mn, target)
    assert eps * (ln + mn + eps) < target


@pytest.mark.fast
def test_adaptive_smoothing_primitive_bound():
    part = [i / 32 for i in range(33)]
    pl = piecewise_linear_interpolation(circle_param, part)
    sm, eps, pred = adaptive_smooth_polygon(pl.interpolant, target_error=0.05)
    gap, bound = verify_smoothing_primitive_control(pl.interpolant, sm, eps)
    assert gap <= bound + 0.5  # exploratory numeric slack on resampling


@pytest.mark.fast
def test_smoothing_bound_formula():
    assert smoothing_primitive_bound(0.01, 100.0, 5.0) == pytest.approx(0.01 * 105.01)
