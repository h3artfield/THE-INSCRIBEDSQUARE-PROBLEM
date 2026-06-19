import pytest

from squarepeg.rough_area.second_level import antisymmetric_area_increment, polygon_area_second_level


@pytest.mark.fast
def test_antisymmetric_segment():
    assert antisymmetric_area_increment((0.0, 0.0), (1.0, 0.0)) == 0.0
    # Start-point Lie bracket (1/2)[x, dx] vanishes when x0 = 0.
    assert antisymmetric_area_increment((0.0, 0.0), (0.0, 1.0)) == 0.0
    assert antisymmetric_area_increment((1.0, 0.0), (1.0, 1.0)) == pytest.approx(0.5)


@pytest.mark.fast
def test_unit_square_area():
    sq = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    assert polygon_area_second_level(sq) == pytest.approx(1.0)
