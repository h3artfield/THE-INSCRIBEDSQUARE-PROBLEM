import math

import pytest

from squarepeg.area_variation.exact_2variation import (
    max_partition_sum_squares,
    squared_2variation,
    two_variation_norm,
)
from squarepeg.variation.p_variation import p_variation_on_partition


@pytest.mark.fast
def test_dp_matches_conforming_partition_when_optimal():
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    sq = max_partition_sum_squares(pts)
    conform = p_variation_on_partition(pts, 2.0) ** 2
    assert sq >= conform - 1e-12


@pytest.mark.fast
def test_zigzag_exceeds_endpoint_distance_squared():
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 0.1), (1.0, 0.1)]
    sq = squared_2variation(pts)
    end_sq = (pts[-1][0] - pts[0][0]) ** 2 + (pts[-1][1] - pts[0][1]) ** 2
    assert sq > end_sq


@pytest.mark.fast
def test_two_var_at_least_diameter_squared():
    pts = [(0.0, 0.0), (0.3, 0.4), (1.0, 0.0)]
    diam = 1.0
    assert squared_2variation(pts) >= diam * diam - 1e-9
