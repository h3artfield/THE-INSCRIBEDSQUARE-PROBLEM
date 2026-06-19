"""T018 controlled C1 polygon smoothing tests (cubic construction)."""

import pytest

from squarepeg.variation.cubic_corner_smoothing import (
    remove_collinear_vertices,
    round_corners_c1_cubic,
    signed_area,
)
from squarepeg.variation.p_variation import euclidean, p_variation, path_difference, total_variation
from squarepeg.variation.smoothing import round_corners_c1

round_corners_c1 = round_corners_c1_cubic  # explicit cubic


def _square() -> list[tuple[float, float]]:
    return [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]


@pytest.mark.fast
def test_remove_collinear():
    pts = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (2.0, 1.0)]
    out = remove_collinear_vertices(pts)
    assert len(out) == 3


@pytest.mark.fast
def test_round_corners_variation_error_small():
    sp = round_corners_c1(_square(), epsilon=0.05)
    assert sp.tv_difference < 0.05 + 1e-6
    assert sp.max_sup_distance < 0.5


@pytest.mark.fast
def test_orientation_preserved():
    sp = round_corners_c1(_square(), epsilon=0.1)
    assert signed_area(sp.smoothed) > 0
    assert signed_area(sp.polygon) > 0


@pytest.mark.fast
def test_q_variation_smoothing_error_decay():
    e1 = round_corners_c1(_square(), epsilon=0.2)
    e2 = round_corners_c1(_square(), epsilon=0.02)
    d1 = path_difference(e1.polygon, e1.smoothed)
    d2 = path_difference(e2.polygon, e2.smoothed)
    assert p_variation(d2, 1.5) <= p_variation(d1, 1.5) + 1e-6


@pytest.mark.fast
def test_common_parametrization_equal_on_bridges():
    sp = round_corners_c1(_square(), epsilon=0.01)
    matches = sum(1 for p, s in zip(sp.polygon, sp.smoothed) if euclidean(p, s) < 1e-12)
    assert matches >= 1
    assert len(sp.polygon) == len(sp.smoothed)
