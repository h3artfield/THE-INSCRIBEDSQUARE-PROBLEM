import math

import pytest

from squarepeg.rough_area.adaptive_smoothing import lifted_primitive_bound
from squarepeg.rough_area.liouville_recovery import recover_primitive
from squarepeg.variation.polygonal_approximation import circle_param, piecewise_linear_interpolation
from squarepeg.variation.smoothing import round_corners_c1
from squarepeg.variation.young_integral import lift_periodic_primitive, max_primitive_gap, primitive_from_points


@pytest.mark.fast
def test_lifted_bound_goes_to_zero():
    eta = 0.01
    period_gap = 0.005
    k = 3
    assert lifted_primitive_bound(eta, period_gap, k) == pytest.approx(eta + 4 * period_gap)


@pytest.mark.fast
def test_refined_primitives_converge_on_circle():
    vals = []
    for n in [16, 32, 64, 128]:
        part = [i / n for i in range(n + 1)]
        pl = piecewise_linear_interpolation(circle_param, part)
        vals.append(recover_primitive(pl.interpolant)[-1])
    assert abs(vals[-1] - vals[-2]) < abs(vals[1] - vals[0])


@pytest.mark.fast
def test_lifted_periodic_extension():
    part = [i / 16 for i in range(17)]
    pl = piecewise_linear_interpolation(circle_param, part)
    base = recover_primitive(pl.interpolant)
    lifted = lift_periodic_primitive(base, periods=3)
    assert len(lifted) > len(base)
    assert lifted[-1] == pytest.approx(base[-1] + 2 * (base[-1] - base[0]), rel=0.01)
