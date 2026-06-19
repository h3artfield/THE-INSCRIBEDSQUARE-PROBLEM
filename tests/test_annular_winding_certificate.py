import pytest

from squarepeg.residual_curves.annular_winding import Annulus, area_lower_bound_from_winding, winding_about_point


@pytest.mark.fast
def test_unit_circle_winding():
    import math

    pts = [(math.cos(t), math.sin(t)) for t in [i * 2 * math.pi / 8 for i in range(9)]]
    w = winding_about_point(pts, (0.0, 0.0))
    assert abs(w) == 1


@pytest.mark.fast
def test_annulus_area_bound_positive():
    a = Annulus(0.5, 1.0)
    assert area_lower_bound_from_winding(1, a) > 0
