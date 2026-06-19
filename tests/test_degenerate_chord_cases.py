import pytest

from squarepeg.area_variation.adversarial_arcs import comb_arc, nested_hook
from squarepeg.area_variation.inequality_certificate import certify_arc
from squarepeg.area_variation.polygonal_arc import PolygonalArc


@pytest.mark.fast
def test_endpoint_chord_collinear_edge():
    """Arc along x-axis; closing chord overlaps first edge — zero area."""
    arc = PolygonalArc.from_points([(0.0, 0.0), (0.5, 0.0), (1.0, 0.0)])
    cert = certify_arc(arc)
    assert cert.area == 0.0
    assert cert.passes


@pytest.mark.fast
def test_vertex_on_chord_comb():
    arc = comb_arc(teeth=5)
    cert = certify_arc(arc)
    assert cert.passes


@pytest.mark.fast
def test_nested_hook_passes():
    cert = certify_arc(nested_hook())
    assert cert.passes
