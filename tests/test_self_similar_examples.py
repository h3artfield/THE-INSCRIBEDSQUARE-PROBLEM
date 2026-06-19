"""Self-similar Koch example tests."""

import math

import pytest

from squarepeg.variation.self_similar_examples import (
    koch_is_nonrectifiable,
    koch_p_variation,
    koch_points,
    koch_variation_exponent,
)


@pytest.mark.fast
def test_koch_variation_exponent():
    assert abs(koch_variation_exponent() - math.log(4) / math.log(3)) < 1e-9


@pytest.mark.fast
def test_koch_total_variation_grows_with_iterations():
    """1-variation (length) grows by factor 4/3 per Koch refinement."""
    from squarepeg.variation.p_variation import p_variation_frac

    v2 = p_variation_frac(koch_points(2), 1.0)
    v3 = p_variation_frac(koch_points(3), 1.0)
    assert v3 > v2


@pytest.mark.fast
def test_koch_p_variation_bounded_above_exponent():
    """For p > log(4)/log(3), chord p-variation on built-in subdivision decreases and stays finite."""
    exp = koch_variation_exponent()
    p = exp + 0.25  # e.g. 1.5
    v2 = koch_p_variation(2, p)
    v3 = koch_p_variation(3, p)
    v4 = koch_p_variation(4, p)
    assert v3 < v2
    assert v4 < v3
    assert v4 > 0


@pytest.mark.fast
def test_koch_nonrectifiable_infinite_length_limit():
    assert koch_is_nonrectifiable(4)
