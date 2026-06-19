import math

import pytest

from squarepeg.area_variation.adversarial_arcs import comb_arc, semicircle_arc, zigzag_chord_crossing
from squarepeg.area_variation.chord_lobes import chord_arc_intersections, decompose_lobes_general_position
from squarepeg.area_variation.exact_2variation import squared_2variation, two_variation_norm
from squarepeg.area_variation.polygonal_arc import PolygonalArc
from squarepeg.area_variation.signed_area import chord_closed_shoelace, relative_area_arc


@pytest.mark.fast
def test_area_equals_chord_shoelace():
    arc = semicircle_arc(32)
    assert relative_area_arc(arc) == pytest.approx(chord_closed_shoelace(arc), rel=1e-10)


@pytest.mark.fast
def test_semicircle_lobe_single():
    arc = semicircle_arc(32)
    hits = chord_arc_intersections(arc)
    assert hits == []
    lobes = decompose_lobes_general_position(arc)
    assert len(lobes) == 1


@pytest.mark.fast
def test_zigzag_has_chord_crossings():
    arc = zigzag_chord_crossing(30)
    hits = chord_arc_intersections(arc)
    assert len(hits) >= 1
