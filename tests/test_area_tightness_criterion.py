import math

import pytest

from squarepeg.area_variation.adversarial_arcs import semicircle_arc
from squarepeg.residual_curves.area_tightness import max_relative_area_on_grid, primitive_oscillation


@pytest.mark.fast
def test_semicircle_relative_area_bounded():
    pts = list(semicircle_arc(32).vertices)
    m = max_relative_area_on_grid(pts)
    assert m < math.pi + 0.1


@pytest.mark.fast
def test_primitive_oscillation_finite():
    pts = list(semicircle_arc(32).vertices)
    assert primitive_oscillation(pts) < 10
