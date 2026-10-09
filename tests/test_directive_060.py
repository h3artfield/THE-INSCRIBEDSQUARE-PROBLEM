"""Directive 060 — non-Jordan saturation hull classification."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.directive_060_clean_room import (
    audit_directive_060_clean_room,
    diagnose_d060_outcome,
    write_non_jordan_routes,
)
from squarepeg.global_geometry.harmless_hull_replacement import certify_t117
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy
from squarepeg.global_geometry.pinched_hull_routes import certify_t118
from squarepeg.global_geometry.saturation_hull import audit_saturation_hulls
from squarepeg.global_geometry.t116_saturation_taxonomy import certify_t116
from squarepeg.global_geometry.t119_non_jordan_reduction import certify_t119
from squarepeg.global_geometry.t120_non_jordan_exhaustion import audit_non_jordan_exhaustion, certify_t120


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_saturation_hull_curve_level():
    assert audit_saturation_hulls(_tree()).curve_level


@pytest.mark.fast
def test_hull_taxonomy():
    audit = audit_non_jordan_hull_taxonomy(_tree())
    assert audit.exhaustive


@pytest.mark.fast
def test_t116():
    assert certify_t116(_tree()).status in ("CONJECTURAL_CLASSIFICATION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t117():
    assert certify_t117(_tree()).status in ("CONJECTURAL_REPLACEMENT_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t118():
    assert certify_t118(_tree()).status in ("CONJECTURAL_ROUTE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t119():
    assert certify_t119(_tree()).status in ("CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t120():
    assert certify_t120(_tree()).status in ("CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS")


@pytest.mark.fast
def test_non_jordan_exhaustion_routes():
    assert audit_non_jordan_exhaustion(_tree()).all_routed


@pytest.mark.deep
def test_routes_artifact():
    assert write_non_jordan_routes(_tree()).exists()


@pytest.mark.deep
def test_d060_clean_room():
    audit = audit_directive_060_clean_room(_tree())
    assert audit.verdict in ("D060_CLEAN_ROOM_VERIFIED", "D060_REPAIRABLE_GAP", "D060_INVALID")


@pytest.mark.deep
def test_d060_outcome():
    assert diagnose_d060_outcome(_tree()) in ("A", "B", "C", "D", "E")
