"""Tests for T037 uniform defect selection."""

import pytest

from squarepeg.robust_degree.uniform_defect_selection import (
    DefectArray,
    alternative_a_holds,
    alternative_b_holds,
    apply_t037_to_polygon_sequence,
    negation_of_b_recursive_selection,
    prove_t037,
)


@pytest.mark.fast
def test_tight_array_gives_alternative_a():
    # a_{n,j} -> 0 as j grows for each n
    values = {(n, j): 2.0 ** (-j - n * 0.01) for n in range(20) for j in range(10)}
    result = prove_t037(DefectArray(values=values), n_max=20, j_max=10)
    assert result.alternative == "A_tight"


@pytest.mark.fast
def test_uniform_defect_array_gives_b():
    values = {(n, j): 0.5 for n in range(30) for j in range(8)}
    result = prove_t037(DefectArray(values=values), n_max=30, j_max=8)
    assert result.alternative == "B_uniform_defect"
    assert result.epsilon_0 > 0


@pytest.mark.fast
def test_nested_subset_construction():
    values = {(n, j): 0.1 / (1 + j) if n < 15 else 2.0 ** (-j) for n in range(25) for j in range(8)}
    tight, j_m, steps = negation_of_b_recursive_selection(DefectArray(values=values))
    assert len(steps) >= 2
    assert len(tight) >= 1


@pytest.mark.fast
def test_apply_to_polygon_array():
    rows = [[0.5 - 0.01 * j for j in range(6)] for _ in range(10)]
    r = apply_t037_to_polygon_sequence(rows)
    assert r.alternative in ("A_tight", "B_uniform_defect")
