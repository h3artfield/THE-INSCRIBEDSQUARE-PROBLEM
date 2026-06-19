import pytest

from squarepeg.rough_area.liouville_recovery import (
    liouville_integral,
    liouville_matches_trapezoid,
    recover_primitive,
)
from squarepeg.variation.young_integral import primitive_from_points


@pytest.mark.fast
def test_liouville_area_identity_unit_square():
    sq = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
    assert liouville_matches_trapezoid(sq)


@pytest.mark.fast
def test_liouville_integral_segment():
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    assert liouville_integral(pts, 0, 2) == pytest.approx(0.0)
    assert liouville_integral(pts, 0, 1) == pytest.approx(0.0)


@pytest.mark.fast
def test_recovery_matches_trapezoid_refined():
    import math

    n = 32
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    ra = recover_primitive(pts)
    rt = primitive_from_points(pts)
    assert all(abs(a - b) < 1e-10 for a, b in zip(ra, rt))
