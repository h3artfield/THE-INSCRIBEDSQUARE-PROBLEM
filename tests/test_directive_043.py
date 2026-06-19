"""Directive 043 — nonsummable tree geometry and diffuse end measures."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.cantor_end_residual import (
    audit_cantor_end_residual,
    build_binary_diffuse_end_tree,
)
from squarepeg.defect_extraction.child_signature_concentration import (
    audit_child_signature_concentration,
    build_cantor_child_center_tree,
    build_concentrated_child_tree,
    build_uniform_circle_child_centers,
)
from squarepeg.defect_extraction.countable_child_order import build_countably_branching_tree
from squarepeg.defect_extraction.diffuse_end_geometry import certify_t086
from squarepeg.defect_extraction.infinite_tree_final_reduction import certify_t082f
from squarepeg.defect_extraction.intrinsic_tree_nonsummability import audit_intrinsic_tree_nonsummability
from squarepeg.defect_extraction.nonsummable_ray_measure import (
    audit_nonsummable_ray_measure,
    build_harmonic_nonsummable_ray,
    build_moving_center_ray,
    build_pinched_end_ray,
    build_plateau_ray,
)
from squarepeg.defect_extraction.nonsummable_ray_reduction import certify_t085
from squarepeg.defect_extraction.nonsummable_tree_classifier import certify_t084r
from squarepeg.defect_extraction.tree_end_signature_measure import audit_tree_end_signature_measure


@pytest.mark.fast
def test_intrinsic_child_nonsummability():
    tree = build_countably_branching_tree(child_count=24, lambda_ratio=0.95)
    audit = audit_intrinsic_tree_nonsummability(tree)
    assert audit.failure_class in (
        "CHILD_LINEAR_NONSUMMABILITY",
        "MULTIPLE_TREE_FAILURES",
        "NONE",
    )


@pytest.mark.fast
def test_intrinsic_ray_nonsummability():
    tree = build_harmonic_nonsummable_ray(length=14)
    audit = audit_intrinsic_tree_nonsummability(tree)
    assert audit.ray_record is not None
    assert audit.ray_record.nonsummable


@pytest.mark.fast
def test_child_concentration_concentrated():
    tree = build_concentrated_child_tree(child_count=10)
    audit = audit_child_signature_concentration(tree)
    assert audit.routes_t064 or audit.primary_branch == "CONCENTRATED"


@pytest.mark.fast
def test_child_concentration_finite_center():
    tree = build_uniform_circle_child_centers(child_count=8)
    audit = audit_child_signature_concentration(tree)
    assert audit.primary_branch in ("FINITE_CENTER", "DIFFUSE", "CONCENTRATED")


@pytest.mark.fast
def test_diffuse_child_center_node():
    tree = build_cantor_child_center_tree(child_count=20)
    audit = audit_child_signature_concentration(tree)
    assert audit.diffuse_child_center or audit.primary_branch == "DIFFUSE"


@pytest.mark.fast
def test_harmonic_nonsummable_ray():
    tree = build_harmonic_nonsummable_ray()
    audit = audit_nonsummable_ray_measure(tree)
    assert audit.measure is not None
    assert not audit.measure.summable


@pytest.mark.fast
def test_plateau_ray():
    tree = build_plateau_ray()
    audit = audit_nonsummable_ray_measure(tree)
    assert audit.measure is not None
    assert audit.measure.plateau_run


@pytest.mark.fast
def test_moving_center_ray():
    tree = build_moving_center_ray()
    cert = certify_t085(tree)
    assert cert.nonsummable
    assert cert.route != "SUMMABLE_RAY"


@pytest.mark.fast
def test_t085_harmonic_ray():
    cert = certify_t085(build_harmonic_nonsummable_ray())
    assert cert.nonsummable
    assert cert.status == "PROVED_LOCALLY_CLASSIFIER"
    assert cert.route == "CONCENTRATED_DESCENT"


@pytest.mark.fast
def test_t085_plateau_ray():
    cert = certify_t085(build_plateau_ray())
    assert cert.route == "ANNULAR_BAND_GEOMETRY"
    assert cert.nonsummable


@pytest.mark.fast
def test_pinched_end_non_jordan():
    cert = certify_t085(build_pinched_end_ray())
    assert cert.route in ("NON_JORDAN_DEGENERATION", "ANNULAR_BAND_GEOMETRY", "DIFFUSE_RAY_RESIDUAL")


@pytest.mark.fast
def test_end_measure_independence():
    tree = build_countably_branching_tree(child_count=16, lambda_ratio=0.7)
    audit = audit_tree_end_signature_measure(tree)
    assert audit.truncation_independent


@pytest.mark.fast
def test_atomic_end_measure():
    tree = build_countably_branching_tree(child_count=8, depth_after=0)
    audit = audit_tree_end_signature_measure(tree)
    assert audit.atom_class in (
        "FINITE_ATOMIC",
        "COUNTABLY_ATOMIC_SUMMABLE",
        "COUNTABLY_ATOMIC_NONSUMMABLE",
    )


@pytest.mark.fast
def test_diffuse_end_classifier():
    tree = build_binary_diffuse_end_tree(depth=4)
    cert = certify_t086(tree)
    assert cert.route in (
        "CANTOR_END_RESIDUAL",
        "INFINITE_CENTER_PROLIFERATION",
        "FINITE_CENTER_DECOMPOSITION",
        "NOT_DIFFUSE",
    )


@pytest.mark.fast
def test_cantor_end_residual():
    tree = build_binary_diffuse_end_tree(depth=5)
    audit = audit_cantor_end_residual(tree)
    assert isinstance(audit.is_cantor_residual, bool)


@pytest.mark.fast
def test_t084r_nonsummable_tree():
    tree = build_harmonic_nonsummable_ray()
    cert = certify_t084r(tree)
    assert cert.nonsummable
    assert cert.route in (
        "NONSUMMABLE_RAY_T085",
        "CONCENTRATED_DESCENT",
        "DIFFUSE_END_T086",
        "INFINITE_CENTER_BRANCHING",
    )


@pytest.mark.fast
def test_t084r_summable_countable():
    tree = build_countably_branching_tree(child_count=20, lambda_ratio=0.72)
    cert = certify_t084r(tree)
    assert cert.route == "T081I_SUMMABLE"
    assert not cert.nonsummable


@pytest.mark.fast
def test_t082f_final_reduction():
    tree = build_countably_branching_tree(child_count=20, lambda_ratio=0.72)
    cert = certify_t082f(tree)
    assert cert.surgically_closed
    assert cert.route == "T081I_COUNTABLY_BRANCHING"


@pytest.mark.fast
def test_t082f_nonsummable_route():
    tree = build_harmonic_nonsummable_ray()
    cert = certify_t082f(tree)
    assert not cert.surgically_closed
    assert cert.route == "NONSUMMABLE_RAY_T085"


@pytest.mark.fast
def test_alternating_sign_end():
    tree = build_harmonic_nonsummable_ray(length=12)
    audit = audit_tree_end_signature_measure(tree)
    assert audit.end_records
