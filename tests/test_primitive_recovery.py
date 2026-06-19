import pytest

from squarepeg.rough_area.primitive_recovery import closed_period_integral, recover_liouville_pl
from squarepeg.rough_area.second_level import liouville_from_second_level_symmetric, polygon_area_second_level


@pytest.mark.fast
def test_pl_shoelace_matches_unit_circle():
    import math

    n = 64
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    assert polygon_area_second_level(pts) == pytest.approx(math.pi, rel=0.02)


@pytest.mark.fast
def test_pl_liouville_integral_unit_circle():
    import math

    n = 64
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    liou = liouville_from_second_level_symmetric(pts)
    assert liou == pytest.approx(-math.pi, rel=0.02)


@pytest.mark.fast
def test_recover_primitive_endpoints():
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    p = recover_liouville_pl(pts)
    assert p[0] == 0.0
