"""Area defect and collapse diagnostics."""

import pytest

from squarepeg.robust_degree.area_defect import alpha_P_delta, polygon_gamma
from squarepeg.robust_degree.collapse_classifier import classify_polygon_collapse


@pytest.mark.fast
def test_alpha_delta_small_on_square():
    verts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    g = polygon_gamma(verts)
    assert alpha_P_delta(g, 0.5) <= 1.0


@pytest.mark.fast
def test_collapse_classification_records_interpretation():
    modes = classify_polygon_collapse(0.0, {"isolated": 1, "converted": 0, "families": 1})
    assert len(modes) >= 1
