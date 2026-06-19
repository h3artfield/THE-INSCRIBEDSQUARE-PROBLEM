"""T035 area-tight diagonal selection."""

import pytest

from squarepeg.robust_degree.area_defect import polygon_gamma
from squarepeg.robust_degree.area_tight_selection import (
    delta_grid,
    negation_not_fixed_scale,
    t035_equivalence_statement,
)


@pytest.mark.fast
def test_delta_grid():
    assert delta_grid(1) == 0.5
    assert delta_grid(2) == 0.25


@pytest.mark.fast
def test_t035_equivalence_documented():
    eq = t035_equivalence_statement()
    assert "area_tight" in eq
    assert "diagonal" in eq
    assert "negation" in eq


@pytest.mark.fast
def test_negation_not_single_scale():
    assert "migrate" in negation_not_fixed_scale().lower()
