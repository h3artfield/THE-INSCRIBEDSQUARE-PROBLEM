import pytest

from squarepeg.variation.cubic_corner_smoothing import round_corners_c1_cubic
from squarepeg.variation.p_variation import path_difference, total_variation


@pytest.mark.fast
def test_smoothing_tolerance_scales():
    sq = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
    e1 = round_corners_c1_cubic(sq, epsilon=0.1)
    e2 = round_corners_c1_cubic(sq, epsilon=0.01)
    d1 = total_variation(path_difference(e1.polygon, e1.smoothed))
    d2 = total_variation(path_difference(e2.polygon, e2.smoothed))
    assert d2 < d1 + 1e-6
