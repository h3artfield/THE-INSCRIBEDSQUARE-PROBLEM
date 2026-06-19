"""Exact component decomposition and master identity tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.exact_component_decomposition import (
    attachment_chain_area_from_deltas,
    component_delta,
    decompose_cyclic_interval,
    master_area_identity,
    pairwise_wedge_area,
    verify_notation_equivalence,
)
from squarepeg.defect_surgery.examples import example_bump_disk, example_bump_polygon
from squarepeg.defect_surgery.exact_component_decomposition import PathComponent
from squarepeg.defect_surgery.nested_forest import PacketForest


@pytest.mark.fast
def test_notation_equivalence():
    assert verify_notation_equivalence([(0, 0), (1, 0), (1, 1)])


@pytest.mark.fast
def test_pairwise_wedge_equals_attachment_area():
    deltas = [(1.0, 0.0), (0.0, 1.0), (-1.0, -1.0)]
    a_z = attachment_chain_area_from_deltas((0.0, 0.0), deltas)
    assert abs(a_z - pairwise_wedge_area(deltas)) < 1e-9


@pytest.mark.fast
def test_master_identity_straight_chords():
    comps = [
        PathComponent("retained", [(0, 0), (1, 0)], component_delta([(0, 0), (1, 0)])),
        PathComponent("crosscut", [(1, 0), (2, 0)], component_delta([(1, 0), (2, 0)])),
        PathComponent("retained", [(2, 0), (3, 0)], component_delta([(2, 0), (3, 0)])),
    ]
    ident = master_area_identity(comps)
    assert ident.exact
    assert abs(ident.chi_curved) < 1e-12


@pytest.mark.fast
def test_cyclic_decomposition_bump():
    forest = PacketForest(disks=[example_bump_disk()])
    decomp = decompose_cyclic_interval(example_bump_polygon(), 0, 6, forest)
    assert any(c.kind == "crosscut" for c in decomp.components)
    ident = master_area_identity(decomp.components)
    assert ident.exact


@pytest.mark.fast
def test_seam_crossing_interval():
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    decomp = decompose_cyclic_interval(square, 3, 1, PacketForest(disks=[]))
    assert decomp.wraps_seam
    ident = master_area_identity(decomp.components)
    assert ident.exact
