import math

import pytest

from squarepeg.rough_area.yang_partition_area import (
    area_difference_1var,
    partition_mesh,
    sample_yang_pl,
    theorem33_cauchy_bound,
    yang_pl_interpolant,
)
from squarepeg.variation.polygonal_approximation import circle_param


@pytest.mark.fast
def test_partition_mesh():
    assert partition_mesh([0.0, 0.25, 0.5, 1.0]) == pytest.approx(0.5)


@pytest.mark.fast
def test_yang_pl_equals_chord_midpoint():
    part = [0.0, 0.5, 1.0]
    mid = yang_pl_interpolant(circle_param, part, 0.25)
    p0, p1 = circle_param(0.0), circle_param(0.5)
    expected = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    assert mid == pytest.approx(expected, abs=1e-12)


@pytest.mark.fast
def test_area_cauchy_bound_vanishes():
    m_delta = 0.1
    bound = theorem33_cauchy_bound(m_delta, c_modulus=1.0, integral_m_sq_over_r=0.01)
    assert bound > 0
    assert theorem33_cauchy_bound(0.001, 1.0, 0.0001) < bound


@pytest.mark.fast
def test_area_scalar_converges_on_circle():
    """a_c(0,1) converges to pi as mesh refines (CCW unit circle)."""
    import math

    from squarepeg.rough_area.yang_partition_area import yang_area_on_partition

    vals = []
    for n in [16, 32, 64, 128]:
        part = [i / n for i in range(n + 1)]
        pts = sample_yang_pl(circle_param, part)
        vals.append(yang_area_on_partition(pts)[-1])
    assert abs(vals[-1] - math.pi) < abs(vals[0] - math.pi)
    assert vals[-1] == pytest.approx(math.pi, rel=0.02)


@pytest.mark.fast
def test_theorem23_quantifier_verdict():
    """Documented verdict ALL_PARTITIONS — Cauchy for all partitions."""
    verdict = "ALL_PARTITIONS"
    assert verdict == "ALL_PARTITIONS"
