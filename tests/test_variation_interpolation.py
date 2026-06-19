"""Interpolation inequality — independent proof validation."""

import pytest

from squarepeg.variation.p_variation import (
    osc,
    p_variation,
    path_difference,
    q_variation_from_p_bound,
)


@pytest.mark.fast
def test_interpolation_inequality_holds_on_samples():
    p, q = 1.25, 1.5
    paths = [
        [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)],
        [(0.0, 0.0), (0.3, 0.2), (0.7, 0.1), (1.0, 0.0)],
    ]
    for pts in paths:
        lhs = p_variation(pts, q)
        rhs = q_variation_from_p_bound(p, q, p_variation(pts, p), osc(pts))
        assert lhs <= rhs + 1e-10


@pytest.mark.fast
def test_difference_qvar_triangle_via_1var():
    """|S-P|_{1-var} <= |S|_{1-var}+|P|_{1-var} (used in T018)."""
    p = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
    s = [(0.0, 0.0), (1.0, 0.0), (0.9, 1.0), (0.0, 1.0), (0.0, 0.0)]
    # common partition by resampling omitted — use equal length
    n = min(len(p), len(s))
    d = path_difference(p[:n], s[:n])
    from squarepeg.variation.p_variation import total_variation

    assert total_variation(d) <= total_variation(p[:n]) + total_variation(s[:n]) + 1e-10
