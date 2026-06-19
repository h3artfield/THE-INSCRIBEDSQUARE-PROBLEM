"""Defect interval and winding tests."""

import math

import pytest

from squarepeg.robust_degree.area_defect import polygon_gamma
from squarepeg.robust_degree.minimal_defect_interval import (
    dyadic_minimize,
    extract_shrinking_witnesses,
    endpoint_chord_correction,
    select_witness_interval,
)
from squarepeg.robust_degree.winding_amplification import (
    amplification_diverges,
    winding_amplification,
)


@pytest.mark.fast
def test_endpoint_correction_identity():
    g = polygon_gamma([(0, 0), (1, 0), (1, 1), (0, 1)])
    c = endpoint_chord_correction(g, 0.1, 0.4)
    assert c >= 0


@pytest.mark.fast
def test_dyadic_minimize():
    g = polygon_gamma([(0, 0), (2, 0), (2, 2), (0, 2)])
    w = select_witness_interval(g, 0.5, 0, 0.01)
    if w:
        m = dyadic_minimize(g, w, 0.01)
        assert m.children_max_area <= w.area + 1e-6


@pytest.mark.fast
def test_winding_amplification_diverges():
    pkt = winding_amplification(lambda t: (math.cos(t), math.sin(t)), 0.1, 0.3, 0.05, 0.01)
    assert amplification_diverges(pkt.r_j, pkt.area_abs)
