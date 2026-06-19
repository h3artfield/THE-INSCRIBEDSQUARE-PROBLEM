"""Directive 028 — infinite intrusion trees."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.infinite_intrusion_tree import (
    audit_infinite_intrusion_tree,
    example_infinite_ray_sequence,
)
from squarepeg.defect_extraction.residual_classifier import classify_residual


@pytest.mark.fast
def test_infinite_nested_ray():
    nodes = example_infinite_ray_sequence(10)
    audit = audit_infinite_intrusion_tree(nodes)
    assert audit.tree_class == "INFINITE_NESTED_RAY"
    residual = classify_residual(infinite=audit)
    assert residual.primary_class == "INFINITE_MULTIGATE_INTRUSION_RAY"
    assert residual.narrower_than_d027
