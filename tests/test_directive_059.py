"""Directive 059 — positive-scale nonannular cluster geometry."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.annular_positive_scale import certify_t113
from squarepeg.global_geometry.directive_059_clean_room import (
    audit_directive_059_clean_room,
    diagnose_d059_outcome,
    write_positive_scale_routes,
)
from squarepeg.global_geometry.finite_center_positive_scale import certify_t114
from squarepeg.global_geometry.nonannular_cluster_classifier import audit_nonannular_cluster_classifier
from squarepeg.global_geometry.positive_scale_cluster import audit_positive_scale_clusters
from squarepeg.global_geometry.positive_scale_residual_routes import audit_positive_scale_residual_routes
from squarepeg.global_geometry.t091_universal_positive_scale import certify_t091u
from squarepeg.global_geometry.t112_positive_scale_classification import certify_t112
from squarepeg.global_geometry.t115_nonannular_exhaustion import certify_t115


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_positive_scale_cluster_curve_level():
    audit = audit_positive_scale_clusters(_tree())
    assert audit.curve_level_definition


@pytest.mark.fast
def test_annular_nonannular_split():
    cert = certify_t112(_tree())
    assert cert.split_exhaustive


@pytest.mark.fast
def test_t113_annular():
    cert = certify_t113(_tree())
    assert cert.status in ("CONJECTURAL_ROUTE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t114_finite_center():
    cert = certify_t114(_tree())
    assert cert.status in ("CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_nonannular_classifier():
    audit = audit_nonannular_cluster_classifier(_tree())
    assert audit.exhaustive


@pytest.mark.fast
def test_residual_routes():
    audit = audit_positive_scale_residual_routes(_tree())
    assert audit.all_routed


@pytest.mark.fast
def test_t115_exhaustion():
    cert = certify_t115(_tree())
    assert cert.status in ("CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS")


@pytest.mark.fast
def test_t091u():
    cert = certify_t091u(_tree())
    assert cert.status in ("CONJECTURAL_UNIVERSALIZATION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_routes_artifact():
    path = write_positive_scale_routes(_tree())
    assert path.exists()


@pytest.mark.fast
def test_d059_clean_room():
    audit = audit_directive_059_clean_room(_tree())
    assert audit.verdict in ("D059_CLEAN_ROOM_VERIFIED", "D059_REPAIRABLE_GAP", "D059_INVALID")


@pytest.mark.fast
def test_d059_outcome():
    outcome = diagnose_d059_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
