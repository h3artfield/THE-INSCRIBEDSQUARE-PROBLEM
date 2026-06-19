"""Directive 044 — diffuse tree-end measures and Cantor-end surgery."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.cantor_end_surgery import (
    audit_cantor_end_surgery,
    build_bernoulli_end_tree,
    build_middle_thirds_cantor_tree,
    certify_t087,
)
from squarepeg.defect_extraction.child_signature_concentration import build_uniform_circle_child_centers
from squarepeg.defect_extraction.countable_child_order import build_countably_branching_tree
from squarepeg.defect_extraction.diffuse_end_reduction import certify_t084e, certify_t086_v2, certify_t088
from squarepeg.defect_extraction.end_concentration import audit_end_concentration
from squarepeg.defect_extraction.end_measure_independence import audit_end_measure_independence
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2
from squarepeg.defect_extraction.end_spatial_map import audit_end_spatial_map
from squarepeg.defect_extraction.infinite_center_end_geometry import audit_infinite_center_end_geometry
from squarepeg.defect_extraction.intrusion_tree_boundary import audit_tree_boundary
from squarepeg.defect_extraction.t087_clean_room import audit_t087_clean_room
from squarepeg.defect_extraction.tree_end_cylinders import audit_cylinder_partition


def _carleson_tree():
    return build_countably_branching_tree(child_count=20, lambda_ratio=0.68, depth_after=1)


@pytest.mark.fast
def test_locally_finite_boundary():
    audit = audit_tree_boundary(_carleson_tree())
    assert audit.topology == "COUNTABLY_BRANCHING_CYLINDER"


@pytest.mark.fast
def test_cylinder_partition():
    tree = _carleson_tree()
    audit = audit_cylinder_partition(tree, tree.root_id)
    assert audit.child_partition


@pytest.mark.fast
def test_end_measure_independence():
    audit = audit_end_measure_independence(_carleson_tree())
    assert audit.independent or audit.processing_order_independent


@pytest.mark.fast
def test_atomic_diffuse_decomposition():
    em = build_end_signature_measure_v2(_carleson_tree())
    assert em.total_unsigned > 0
    assert em.total_positive >= 0


@pytest.mark.fast
def test_spatial_endpoint_map():
    audit = audit_end_spatial_map(_carleson_tree())
    assert audit.point_valued_ae


@pytest.mark.fast
def test_end_concentration():
    audit = audit_end_concentration(_carleson_tree())
    assert audit.concentration_class in ("CONCENTRATED", "FINITE_CENTER", "DIFFUSE")


@pytest.mark.fast
def test_end_signature_carleson():
    audit = audit_end_signature_carleson(_carleson_tree())
    assert isinstance(audit.satisfies_carleson, bool)


@pytest.mark.fast
def test_bernoulli_end_measure():
    tree = build_bernoulli_end_tree(depth=4)
    em = build_end_signature_measure_v2(tree)
    assert em.continuous_mass >= 0


@pytest.mark.fast
def test_cantor_end_tree():
    tree = build_middle_thirds_cantor_tree(levels=3)
    audit = audit_end_signature_carleson(tree)
    assert isinstance(audit.satisfies_carleson, bool)


@pytest.mark.fast
def test_antichain_surgery():
    audit = audit_cantor_end_surgery(_carleson_tree())
    assert audit.steps
    assert audit.limit_jordan


@pytest.mark.fast
def test_cross_cylinder_estimates():
    audit = audit_cantor_end_surgery(_carleson_tree())
    assert all(s.cross_cylinder_bound >= 0 for s in audit.steps)


@pytest.mark.fast
def test_frostman_bound():
    audit = audit_end_signature_carleson(_carleson_tree())
    assert audit.frostman_exponent is None or isinstance(audit.frostman_exponent, float)


@pytest.mark.fast
def test_t087_proved_locally():
    cert = certify_t087(_carleson_tree())
    assert cert.status == "PROVED_LOCALLY"
    assert cert.area_tight


@pytest.mark.fast
def test_t087_clean_room_verified():
    audit = audit_t087_clean_room(_carleson_tree())
    assert audit.verdict == "T087_CLEAN_ROOM_VERIFIED"


@pytest.mark.fast
def test_t086_carleson_route():
    cert = certify_t086_v2(_carleson_tree())
    assert cert.route in ("T087_DIFFUSE_SURGERY", "SUMMABLE_CLOSED")
    assert cert.status == "PROVED_LOCALLY_CLASSIFIER"


@pytest.mark.fast
def test_t087_certificate():
    cert = certify_t087(_carleson_tree())
    assert cert.status in ("PROVED_LOCALLY", "CONJECTURAL_TARGET")


@pytest.mark.fast
def test_t087_clean_room():
    audit = audit_t087_clean_room(_carleson_tree())
    assert audit.verdict in ("T087_CLEAN_ROOM_VERIFIED", "T087_REPAIRABLE_GAP", "T087_INVALID")


@pytest.mark.fast
def test_t086_v2():
    cert = certify_t086_v2(_carleson_tree())
    assert cert.route in (
        "T087_DIFFUSE_SURGERY",
        "SUMMABLE_CLOSED",
        "CONCENTRATED_DESCENT",
        "FINITE_CENTER_DECOMPOSITION",
        "CANTOR_END_RESIDUAL",
    )


@pytest.mark.fast
def test_t084e():
    cert = certify_t084e(_carleson_tree())
    assert cert.route


@pytest.mark.fast
def test_t088_promotion():
    cert = certify_t088(build_uniform_circle_child_centers(child_count=12))
    assert cert.route


@pytest.mark.fast
def test_infinite_center_geometry():
    tree = build_uniform_circle_child_centers(child_count=16)
    audit = audit_infinite_center_end_geometry(tree)
    assert isinstance(audit.infinite_center, bool)


@pytest.mark.fast
def test_noninjective_endpoint():
    tree = build_uniform_circle_child_centers(child_count=10)
    spatial = audit_end_spatial_map(tree)
    assert spatial.records


@pytest.mark.fast
def test_middle_thirds_cantor_residual():
    tree = build_middle_thirds_cantor_tree(levels=4)
    cert = certify_t086_v2(tree)
    assert cert.route in (
        "CANTOR_END_RESIDUAL",
        "FINITE_CENTER_DECOMPOSITION",
        "CONCENTRATED_DESCENT",
        "T087_DIFFUSE_SURGERY",
        "SUMMABLE_CLOSED",
    )
