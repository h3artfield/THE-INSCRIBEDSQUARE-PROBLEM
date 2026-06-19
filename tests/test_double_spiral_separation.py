import math

import pytest

from squarepeg.residual_curves.double_spiral import (
    d_separation,
    gamma_minus,
    gamma_plus,
    r_outer,
)


@pytest.mark.fast
def test_arm_separation_positive():
    for th in [10.0, 20.0, 50.0]:
        assert d_separation(th) > 0
        rp = math.hypot(*gamma_plus(th))
        rm = math.hypot(*gamma_minus(th))
        assert rm < rp - 0.5 * d_separation(th)


@pytest.mark.fast
def test_opposite_points_separated():
    th = 20.0
    p0 = gamma_plus(th)
    p1 = gamma_plus(th + math.pi)
    dist = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    assert dist >= 0.5 * r_outer(th)
