import pytest

from squarepeg.area_variation.adversarial_arcs import semicircle_arc
from squarepeg.rough_area.adaptive_smoothing import adaptive_smooth_polygon, verify_smoothing_primitive_control
from squarepeg.rough_area.liouville_recovery import recover_primitive


@pytest.mark.fast
def test_smoothing_chain_runs_with_adaptive_tolerance():
    arc = semicircle_arc(16)
    verts = list(arc.vertices)
    sm, eps, pred = adaptive_smooth_polygon(verts, target_error=1e-3)
    assert len(sm.smoothed) >= len(verts)
    assert eps > 0 and pred > 0
    gap, bound = verify_smoothing_primitive_control(verts, sm, eps)
    assert gap < float("inf")


@pytest.mark.fast
def test_polygon_primitives_bounded():
    verts = list(semicircle_arc(64).vertices)
    prim = recover_primitive(verts)
    assert max(prim) - min(prim) < 10
