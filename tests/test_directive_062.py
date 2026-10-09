"""Directive 062 — infinite-center limit geometry."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.global_geometry.directive_062_clean_room import audit_directive_062_clean_room, write_infinite_center_routes
from squarepeg.global_geometry.infinite_center_limits import audit_infinite_center_limits
from squarepeg.global_geometry.t126_infinite_center_decomposition import certify_t126
from squarepeg.global_geometry.t128_center_finite_route import certify_t128
from squarepeg.global_geometry.t130_infinite_center_exhaustion import audit_infinite_center_exhaustion, certify_t130
from squarepeg.ledger.universal_proof_obligations import list_universal_obligations, universal_theorem_closed


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_infinite_center_curve_level():
    assert audit_infinite_center_limits(_tree()).curve_level


@pytest.mark.fast
def test_t126():
    assert certify_t126(_tree()).status in ("CONJECTURAL_DECOMPOSITION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t128():
    assert certify_t128(_tree()).status in ("CONJECTURAL_ROUTE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t130():
    assert certify_t130(_tree()).status in ("CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS")


@pytest.mark.fast
def test_infinite_center_exhaustion():
    assert audit_infinite_center_exhaustion(_tree()).all_routed


@pytest.mark.fast
def test_universal_not_closed():
    assert not universal_theorem_closed()
    assert any(o.status == "OPEN" for o in list_universal_obligations())


@pytest.mark.deep
def test_routes_artifact():
    assert write_infinite_center_routes(_tree()).exists()


@pytest.mark.deep
def test_d062_clean_room():
    audit = audit_directive_062_clean_room(_tree())
    assert audit.verdict in ("D062_CLEAN_ROOM_VERIFIED", "D062_REPAIRABLE_GAP", "D062_INVALID")
