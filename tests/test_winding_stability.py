"""Tests for winding stability."""

import pytest

from squarepeg.residual_curves.annular_winding import winding_about_point
from squarepeg.residual_curves.canonical import CanonicalDoubleSpiral
from squarepeg.residual_curves.protected_annuli import annulus_for_turn
from squarepeg.residual_curves.winding_stability import (
    annulus_test_point,
    winding_stable_under_uniform_closeness,
)


@pytest.mark.fast
def test_identical_curves_winding_stable():
    canon = CanonicalDoubleSpiral()
    ann = annulus_for_turn(0)
    pts = canon.closed_polygon_with_connector(turns=6)
    center = annulus_test_point(ann)
    closed = pts + [pts[0]]
    ref = winding_about_point(closed, center)
    assert winding_stable_under_uniform_closeness(
        pts, pts, ann, reference_winding=ref
    )
