"""Polygonal approximation tests."""

import pytest

from squarepeg.variation.polygonal_approximation import chord_polygon, mesh_size


@pytest.mark.fast
def test_chord_polygon_preserves_order():
    pts = [(0, 0), (1, 0), (1, 1)]
    assert chord_polygon(pts) == pts


@pytest.mark.fast
def test_mesh_size():
    pts = [(0, 0), (1, 0), (1, 1)]
    assert mesh_size(pts) == 1.0
