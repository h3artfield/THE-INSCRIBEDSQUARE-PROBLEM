import pytest

from squarepeg.residual_curves.double_spiral import annulus_area_between_arms


@pytest.mark.fast
def test_arm_annulus_area_finite_sum():
    total = sum(annulus_area_between_arms(10.0 + k) for k in range(100))
    assert 0 < total < 1000
