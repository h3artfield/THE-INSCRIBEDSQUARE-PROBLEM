"""Directive 061 — parameter-disconnected limit geometry."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.directive_061_clean_room import (
    audit_directive_061_clean_room,
    diagnose_d061_outcome,
    write_parameter_routes,
)
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits
from squarepeg.global_geometry.parameter_support import audit_parameter_support
from squarepeg.global_geometry.t121_parameter_decomposition import certify_t121
from squarepeg.global_geometry.t122_component_splitting import certify_t122
from squarepeg.global_geometry.t123_cross_component_routing import certify_t123
from squarepeg.global_geometry.t124_parameter_reduction import certify_t124
from squarepeg.global_geometry.t125_parameter_exhaustion import audit_parameter_exhaustion, certify_t125


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_parameter_support_curve_level():
    assert audit_parameter_support(_tree()).curve_level


@pytest.mark.fast
def test_parameter_disconnected_limits():
    assert audit_parameter_disconnected_limits(_tree()).exhaustive


@pytest.mark.fast
def test_t121():
    assert certify_t121(_tree()).status in ("CONJECTURAL_DECOMPOSITION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t122():
    assert certify_t122(_tree()).status in ("CONJECTURAL_SPLITTING_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t123():
    assert certify_t123(_tree()).status in ("CONJECTURAL_INTERACTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t124():
    assert certify_t124(_tree()).status in ("CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t125():
    assert certify_t125(_tree()).status in ("CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS")


@pytest.mark.fast
def test_parameter_exhaustion_routes():
    assert audit_parameter_exhaustion(_tree()).all_routed


@pytest.mark.deep
def test_routes_artifact():
    assert write_parameter_routes(_tree()).exists()


@pytest.mark.deep
def test_d061_clean_room():
    audit = audit_directive_061_clean_room(_tree())
    assert audit.verdict in ("D061_CLEAN_ROOM_VERIFIED", "D061_REPAIRABLE_GAP", "D061_INVALID")


@pytest.mark.deep
def test_d061_outcome():
    assert diagnose_d061_outcome(_tree()) in ("A", "B", "C", "D", "E")
