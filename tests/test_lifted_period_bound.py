"""Lifted-period primitive convergence bound (T017-R1)."""

import pytest

from squarepeg.variation.young_integral import lift_periodic_primitive


def lifted_period_bound(eta_n: float, i_n: float, i: float, K: float) -> float:
    """sup_{|t|<=K} |f_n(t)-f(t)| <= eta_n + N_K |I_n - I|."""
    import math

    n_k = math.ceil(K / (2 * math.pi)) + 1
    return eta_n + n_k * abs(i_n - i)


@pytest.mark.fast
def test_period_count_bound():
    assert lifted_period_bound(0.01, 1.0, 1.0, 10.0) == pytest.approx(0.01, abs=1e-9)


@pytest.mark.fast
def test_period_count_grows_with_k():
    b1 = lifted_period_bound(0.0, 1.0, 0.0, 6.28)
    b2 = lifted_period_bound(0.0, 1.0, 0.0, 100.0)
    assert b2 > b1


@pytest.mark.fast
def test_lifted_primitive_structure():
    base = [0.0, 0.5, 1.0, 1.5]
    lifted = lift_periodic_primitive(base, periods=2)
    assert len(lifted) == len(base) * 2 - 1
    assert lifted[-1] > lifted[0]
