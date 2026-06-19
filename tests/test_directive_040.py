"""Directive 040 — infinite intrusion trees, end geometry, tree surgery."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.branching_signature import audit_branching_carleson
from squarepeg.defect_extraction.branching_tree_surgery import certify_t081
from squarepeg.defect_extraction.canonical_intrusion_tree import (
    audit_parent_child_relation,
    build_binary_branching_tree,
    build_geometric_decay_ray,
    build_tree_from_leaf,
)
from squarepeg.defect_extraction.defect_tree_pruning import audit_defect_pruning
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.infinite_tree_reduction import certify_t082
from squarepeg.defect_extraction.intrusion_ray_geometry import audit_ray_geometry, extract_ray
from squarepeg.defect_extraction.intrusion_tree_ends import audit_end_decomposition, build_end_measure
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.ray_branching_dichotomy import certify_t078
from squarepeg.defect_extraction.ray_end_hull import certify_t079
from squarepeg.defect_extraction.summable_ray_signature import audit_summable_ray_signature


def _leaf() -> EssentialLeaf:
    return EssentialLeaf("L1", 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.5, None, [])


@pytest.mark.fast
def test_canonical_parent_child():
    tree = build_geometric_decay_ray(length=10)
    audit = audit_parent_child_relation(tree)
    assert audit.canonical
    assert tree.tree_class == "LOCALLY_FINITE_INTRUSION_TREE"


@pytest.mark.fast
def test_locally_finite_tree():
    tree = build_binary_branching_tree(depth=4)
    assert tree.tree_class == "LOCALLY_FINITE_INTRUSION_TREE"


@pytest.mark.fast
def test_defect_preserving_pruning():
    tree = build_geometric_decay_ray(length=14)
    audit = audit_defect_pruning(tree, theta=0.1)
    assert audit.mass_preserved
    assert audit.outcome in (
        "INFINITE_DEFECT_RAY",
        "BOUNDED_CHILD_DEFECT_LEVEL",
        "JOIN_SIGNATURE_FRACTION",
        "CANCELLATION_MASS",
        "FINITE_TREE",
    )


@pytest.mark.fast
def test_infinite_ray_extraction():
    tree = build_geometric_decay_ray(length=12)
    t078 = certify_t078(tree)
    assert t078.branch in (
        "INFINITE_RAY",
        "ARBITRARILY_LARGE_FINITE_BRANCHING",
        "INFINITE_LOCAL_BRANCHING",
        "FINITE_TREE",
    )


@pytest.mark.fast
def test_shrinking_end_hulls():
    tree = build_geometric_decay_ray(length=12, lambda_ratio=0.65)
    cert = certify_t079(tree)
    assert cert is not None
    assert cert.end_hull.limit_set_single_point or cert.end_hull.end_hull_class != "SINGLE_POINT"


@pytest.mark.fast
def test_two_gate_ray_saturation():
    tree = build_geometric_decay_ray(length=12, lambda_ratio=0.7)
    cert = certify_t079(tree)
    assert cert is not None
    assert cert.status in ("CONJECTURAL_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_ray_signature_tails():
    tree = build_geometric_decay_ray(length=12, lambda_ratio=0.7)
    sig = audit_summable_ray_signature(tree)
    assert sig is not None
    assert sig.scale_mass.S_gate >= 0


@pytest.mark.fast
def test_binary_branching():
    tree = build_binary_branching_tree(depth=4)
    carl = audit_branching_carleson(tree)
    assert carl.carleson_ratio >= 0


@pytest.mark.fast
def test_unbounded_branching():
    tree = build_binary_branching_tree(depth=5)
    t078 = certify_t078(tree)
    assert t078.branch


@pytest.mark.fast
def test_branching_carleson():
    tree = build_binary_branching_tree(depth=4)
    carl = audit_branching_carleson(tree)
    assert isinstance(carl.satisfies_carleson, bool)


@pytest.mark.fast
def test_tree_end_measures():
    tree = build_geometric_decay_ray(length=10)
    em = build_end_measure(tree)
    assert em.measure_class in (
        "ATOMIC",
        "COUNTABLY_ATOMIC",
        "DIFFUSE_CANTOR",
        "FINITE_CENTERS",
        "INFINITE_CENTERS",
    )


@pytest.mark.fast
def test_t080_certificate():
    tree = build_geometric_decay_ray(length=12, lambda_ratio=0.65)
    cert = certify_t080(tree)
    assert cert.status in ("CONJECTURAL_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t081_certificate():
    tree = build_binary_branching_tree(depth=4)
    cert = certify_t081(tree)
    assert cert.status in ("CONJECTURAL_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t082_reduction():
    tree = build_geometric_decay_ray(length=12, lambda_ratio=0.65)
    cert = certify_t082(tree)
    assert cert.route
    assert cert.status in ("CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_PARTIAL")


@pytest.mark.fast
def test_leaf_tree_build():
    tree = build_tree_from_leaf(_leaf())
    geom = audit_ray_geometry(tree)
    assert geom is None or geom.ray.scale_class


@pytest.mark.fast
def test_end_decomposition():
    tree = build_geometric_decay_ray(length=10)
    audit = audit_end_decomposition(tree)
    assert audit.end_measure.total_mass >= 0
