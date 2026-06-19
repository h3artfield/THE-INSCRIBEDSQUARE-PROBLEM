"""Directive 042 — countably branching intrusion trees."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.canonical_intrusion_tree import build_binary_branching_tree
from squarepeg.defect_extraction.child_center_measure import audit_child_center_measures
from squarepeg.defect_extraction.child_l1_signature import audit_child_l1_signature_v2
from squarepeg.defect_extraction.countable_child_identity import audit_countable_child_identity, wedge_tail_bound
from squarepeg.defect_extraction.countable_child_order import (
    build_countably_branching_tree,
    canonical_child_order,
    extract_countable_family,
)
from squarepeg.defect_extraction.countable_child_surgery import audit_countable_child_surgery
from squarepeg.defect_extraction.diffuse_end_classifier import classify_diffuse_ends
from squarepeg.defect_extraction.infinite_local_branching_reduction import certify_t082i, certify_t084
from squarepeg.defect_extraction.mixed_tree_exhaustion import audit_mixed_exhaustion, build_mixed_truncation
from squarepeg.defect_extraction.nonsummable_child_node import audit_nonsummable_child_nodes
from squarepeg.defect_extraction.t081i_clean_room import audit_t081i_clean_room
from squarepeg.defect_extraction.t081i_proof import certify_t081i_v2


def _countable_tree():
    return build_countably_branching_tree(child_count=24, lambda_ratio=0.72, depth_after=1)


@pytest.mark.fast
def test_canonical_child_order():
    tree = _countable_tree()
    fam = extract_countable_family(tree, tree.root_id)
    assert fam is not None
    assert fam.canonical_order


@pytest.mark.fast
def test_absolute_wedge_convergence():
    tree = _countable_tree()
    fam = extract_countable_family(tree, tree.root_id)
    audit = audit_countable_child_identity(fam)
    assert audit.wedge_bound_valid
    assert audit.tail.absolute_convergence


@pytest.mark.fast
def test_child_tail_estimates():
    tree = _countable_tree()
    fam = extract_countable_family(tree, tree.root_id)
    audit = audit_countable_child_identity(fam)
    bound = wedge_tail_bound(audit.tail.L_v, audit.tail.tau_N)
    assert audit.tail.wedge_tail_bound <= bound + 1e-6


@pytest.mark.fast
def test_geometric_child_mass_implies_l1():
    tree = _countable_tree()
    l1 = audit_child_l1_signature_v2(tree)
    assert l1.global_l1


@pytest.mark.fast
def test_infinite_child_jordan_limit():
    tree = _countable_tree()
    fam = extract_countable_family(tree, tree.root_id)
    surg = audit_countable_child_surgery(fam)
    assert surg.limit_jordan


@pytest.mark.fast
def test_mixed_finite_countable_tree():
    tree = _countable_tree()
    mixed = build_mixed_truncation(tree, D=2, N=8)
    assert mixed.finite
    assert mixed.jordan


@pytest.mark.fast
def test_two_parameter_exhaustion():
    audit = audit_mixed_exhaustion(_countable_tree())
    assert audit.truncations
    assert audit.signature_represented


@pytest.mark.fast
def test_harmonic_child_scales():
    tree = build_countably_branching_tree(child_count=20, lambda_ratio=0.75)
    l1 = audit_child_l1_signature_v2(tree)
    assert l1.uniform_local


@pytest.mark.fast
def test_geometric_child_scales():
    tree = build_countably_branching_tree(child_count=18, lambda_ratio=0.68)
    fam = extract_countable_family(tree, tree.root_id)
    assert fam.accumulation_labels


@pytest.mark.fast
def test_diffuse_child_center():
    tree = build_countably_branching_tree(child_count=30, lambda_ratio=0.7)
    audit = audit_child_center_measures(tree)
    assert audit.primary_class


@pytest.mark.fast
def test_atomic_end_measure():
    tree = build_countably_branching_tree(child_count=12, lambda_ratio=0.7, depth_after=0)
    end = classify_diffuse_ends(tree)
    assert end.end_atom_class


@pytest.mark.fast
def test_diffuse_end_measure():
    tree = build_countably_branching_tree(child_count=28, lambda_ratio=0.65)
    end = classify_diffuse_ends(tree)
    assert end.spatial_class


@pytest.mark.fast
def test_nonsummable_child_detection():
    tree = build_countably_branching_tree(child_count=24, lambda_ratio=0.95)
    ns = audit_nonsummable_child_nodes(tree, eta_0=0.01)
    assert isinstance(ns.any_nonsummable, bool)


@pytest.mark.fast
def test_t081i_certificate():
    cert = certify_t081i_v2(_countable_tree())
    assert cert.status == "PROVED_LOCALLY"
    assert cert.area_tight


@pytest.mark.fast
def test_t081i_clean_room():
    audit = audit_t081i_clean_room(_countable_tree())
    assert audit.verdict == "T081I_CLEAN_ROOM_VERIFIED"


@pytest.mark.fast
def test_t084_classifier():
    cert = certify_t084(_countable_tree())
    assert cert.route


@pytest.mark.fast
def test_t082i_reduction():
    cert = certify_t082i(_countable_tree())
    assert cert.t081i


@pytest.mark.fast
def test_binary_tree_still_t081():
    from squarepeg.defect_extraction.branching_tree_area_tightness import certify_t081_v2

    cert = certify_t081_v2(build_binary_branching_tree(depth=4))
    assert cert.status == "PROVED_LOCALLY"
