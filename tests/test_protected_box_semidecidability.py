"""T034 semidecidability characterization."""

import pytest

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.robust_degree.semialgebraic_degree import (
    build_formula_from_rational_box,
    square_map_polynomial_degree,
    t034_semidecidability_statement,
)


@pytest.mark.fast
def test_polynomial_degree_four():
    assert square_map_polynomial_degree() == 4


@pytest.mark.fast
def test_semialgebraic_formula_builds():
    poly = PolygonCurve([(0, 0), (2, 0), (2, 2), (0, 2)])
    from fractions import Fraction

    f = build_formula_from_rational_box(
        poly, (0, 1, 2, 3), ((Fraction(1, 4), Fraction(3, 4)),) * 4, Fraction(1, 100)
    )
    assert f.degree_nonzero
    assert "RCF" in f.to_dict()["field"]


@pytest.mark.fast
def test_t034_statement_nonempty():
    assert "openness" in t034_semidecidability_statement().lower()
