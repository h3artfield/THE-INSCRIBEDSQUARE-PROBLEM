import math

import pytest

from squarepeg.rough_area.liouville_recovery import closed_period_integral, recover_primitive


def _circle(t: float, clockwise: bool = False) -> tuple[float, float]:
    ang = -2 * math.pi * t if clockwise else 2 * math.pi * t
    return (math.cos(ang), math.sin(ang))


@pytest.mark.fast
def test_ccw_circle_closed_integral_symbolic():
    """
    CCW unit circle: oint xi dx = -pi (Green / AI convention).

    Symbolically: x=cos 2pi t, xi=sin 2pi t =>
    int xi dx = int sin d(cos) = -int 2pi sin^2(2pi t) dt = -pi on [0,1].
    """
    n = 256
    pts = [_circle(i / n) for i in range(n + 1)]
    val = closed_period_integral(pts)
    assert val == pytest.approx(-math.pi, rel=0.01)


@pytest.mark.fast
def test_cw_circle_reverses_sign():
    n = 256
    pts = [_circle(i / n, clockwise=True) for i in range(n + 1)]
    ccw = closed_period_integral([_circle(i / n) for i in range(n + 1)])
    cw = closed_period_integral(pts)
    assert cw == pytest.approx(-ccw, rel=0.02)


@pytest.mark.fast
def test_area_formula_gives_same_sign():
    n = 128
    pts = [_circle(i / n) for i in range(n + 1)]
    prim = recover_primitive(pts)
    assert prim[-1] == pytest.approx(-math.pi, rel=0.02)
