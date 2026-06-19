"""Defect lobe tree tests."""

import pytest

from squarepeg.robust_degree.defect_lobe_tree import build_lobe_tree, unbounded_area_forces_combinatorics
from squarepeg.robust_degree.nested_lobe_class import belongs_to_D_nest


@pytest.mark.fast
def test_lobe_tree_builds():
    pts = [(0, 0), (1, 0), (1, 1), (0.5, 0.5), (0, 1)]
    tree = build_lobe_tree(pts, max_depth=3)
    assert tree.max_depth >= 1


@pytest.mark.fast
def test_nested_lobe_class():
    pts = [(0, 0), (1, 0), (0.5, 0.5), (0, 1), (0, 0)]
    tree = build_lobe_tree(pts, max_depth=4)
    assert isinstance(belongs_to_D_nest(tree), bool)
