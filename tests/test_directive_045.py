"""Directive 045 — non-Carleson Cantor ends and tangent trees."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.bad_end_cylinders import audit_bad_end_cylinders
from squarepeg.defect_extraction.cantor_end_surgery import build_middle_thirds_cantor_tree
from squarepeg.defect_extraction.countable_child_order import build_countably_branching_tree
from squarepeg.defect_extraction.end_density_improvement import audit_end_density_improvement
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.finite_center_end_rigidity import certify_t089
from squarepeg.defect_extraction.frostman_end_criterion import certify_t090
from squarepeg.defect_extraction.noncarleson_cantor_tangent import (
    audit_noncarleson_cantor_tangent,
    build_variable_ratio_cantor_tree,
)
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density
from squarepeg.defect_extraction.noncarleson_end_reduction import certify_t084c, certify_t086r
from squarepeg.defect_extraction.normalized_end_tangent import normalize_bad_cylinder
from squarepeg.defect_extraction.tangent_end_classifier import audit_tangent_end_classifier
from squarepeg.defect_extraction.tangent_tree_compactness import audit_tangent_tree_compactness


def _carleson_tree():
    return build_countably_branching_tree(child_count=20, lambda_ratio=0.68, depth_after=1)


def _noncarleson_cantor():
    return build_variable_ratio_cantor_tree(levels=4, ratio=0.58)


@pytest.mark.fast
def test_noncarleson_density_carleson_tree():
    audit = audit_noncarleson_end_density(_carleson_tree())
    assert audit.failure_class == "CARLESON_SATISFIED"


@pytest.mark.fast
def test_noncarleson_density_cantor_tree():
    audit = audit_noncarleson_end_density(_noncarleson_cantor())
    assert audit.intrinsically_non_carleson


@pytest.mark.fast
def test_bad_cylinder_antichain():
    audit = audit_bad_end_cylinders(_noncarleson_cantor())
    assert audit.levels
    assert audit.child_order_independent


@pytest.mark.fast
def test_normalized_tangent():
    tree = _noncarleson_cantor()
    bad = audit_bad_end_cylinders(tree, thresholds=[2.0])
    if bad.levels[0].bad_cylinders:
        v = bad.levels[0].bad_cylinders[0].node_id
        tangent = normalize_bad_cylinder(tree, v)
        assert tangent.nodes


@pytest.mark.fast
def test_tangent_compactness():
    audit = audit_tangent_tree_compactness(_noncarleson_cantor())
    assert audit.sequence is not None


@pytest.mark.fast
def test_tangent_classifier():
    cls = audit_tangent_end_classifier(_noncarleson_cantor())
    assert cls.primary


@pytest.mark.fast
def test_frostman_criterion():
    cert = certify_t090(_carleson_tree())
    assert cert.frostman in ("SUBCRITICAL", "CRITICAL", "SUPERCRITICAL")


@pytest.mark.fast
def test_density_improvement():
    audit = audit_end_density_improvement(_noncarleson_cantor())
    assert audit.steps


@pytest.mark.fast
def test_cantor_tangent_residual():
    audit = audit_noncarleson_cantor_tangent(_noncarleson_cantor())
    assert isinstance(audit.is_cantor_tangent, bool)


@pytest.mark.fast
def test_middle_thirds_noncarleson():
    tree = build_middle_thirds_cantor_tree(levels=4)
    nc = audit_noncarleson_end_density(tree)
    assert nc.failure_class != "CARLESON_SATISFIED" or not audit_end_signature_carleson(tree).satisfies_carleson


@pytest.mark.fast
def test_t086r_cantor_route():
    cert = certify_t086r(_noncarleson_cantor())
    assert cert.route in (
        "NONCARLESON_CANTOR_END_TANGENT",
        "CONCENTRATED_DESCENT",
        "FINITE_CENTER_REDUCTION",
        "INFINITE_CENTER_TANGENT",
        "ATOMIC_RAY_TANGENT",
    )


@pytest.mark.fast
def test_t084c_reduction():
    cert = certify_t084c(_noncarleson_cantor())
    assert cert.route in ("CANTOR_TANGENT", "T086R_TANGENT", "T080_T081I_T087_CLOSED")


@pytest.mark.fast
def test_carleson_tree_t086r_closed():
    cert = certify_t086r(_carleson_tree())
    assert cert.route == "T087_CLOSED"


@pytest.mark.fast
def test_finite_center_rigidity_attempt():
    tree = build_middle_thirds_cantor_tree(levels=3)
    seq = audit_tangent_tree_compactness(tree, A=2.0)
    if seq.sequence and seq.sequence.tangents:
        cert = certify_t089(tree, seq.sequence.tangents[0])
        assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")
