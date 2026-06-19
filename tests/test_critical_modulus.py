import math
import pytest

from squarepeg.rough_area.critical_modulus import log_modulus, modulus_integral_finite, vanishing_2_var_bound


@pytest.mark.fast
def test_log_modulus_alpha_gt_half():
    assert modulus_integral_finite(0.6)
    assert not modulus_integral_finite(0.4)


@pytest.mark.fast
def test_vanishing_bound_scales():
    assert vanishing_2_var_bound(0.1, 2.0) == pytest.approx(0.2)
