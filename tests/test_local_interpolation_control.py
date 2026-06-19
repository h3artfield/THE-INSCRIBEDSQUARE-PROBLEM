import pytest

from squarepeg.area_variation.exact_2variation import squared_2variation
from squarepeg.variation.polygonal_approximation import circle_param, piecewise_linear_interpolation


@pytest.mark.fast
def test_pl_variation_at_partition_points_bounded():
    """PL 2-var squared at mesh points is bounded by conforming partition sum."""
    for n in [16, 32, 64]:
        part = [i / n for i in range(n + 1)]
        pl = piecewise_linear_interpolation(circle_param, part)
        sq = squared_2variation(pl.interpolant)
        assert sq <= 4 * 3.15  # circle 2-var^2 ~ (2)^2 = 4


@pytest.mark.fast
def test_mesh_refinement_variation_stabilizes():
    vals = []
    for n in [8, 16, 32, 64, 128]:
        part = [i / n for i in range(n + 1)]
        pl = piecewise_linear_interpolation(circle_param, part)
        vals.append(squared_2variation(pl.interpolant))
    assert abs(vals[-1] - vals[-2]) < abs(vals[1] - vals[0])
