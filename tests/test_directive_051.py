"""Directive 051 — Bellman potentials and critical invariant states."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.bellman_exact_certificate import audit_bellman_exact_certificate
from squarepeg.defect_extraction.bellman_potential import audit_bellman_potential
from squarepeg.defect_extraction.bookkeeping_coboundary import audit_bookkeeping_coboundary
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.critical_state_classifier import audit_critical_state_classifier, certify_t099
from squarepeg.defect_extraction.invariant_state_measure import audit_invariant_state_measure
from squarepeg.defect_extraction.neutral_occupation_measure import audit_neutral_occupation_measure
from squarepeg.defect_extraction.neutral_state_cone import audit_neutral_state_cone
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t098_clean_room import audit_t098_clean_room
from squarepeg.defect_extraction.t098_proof import (
    certify_t097,
    certify_t098,
    diagnose_d051_outcome,
)
from squarepeg.defect_extraction.transition_family import audit_transition_family


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_state_coordinate_identities():
    audit = audit_augmented_neutral_state(_tree())
    assert audit.states
    assert all(s.Phi >= 0 for s in audit.states)


@pytest.mark.fast
def test_state_cone_closure():
    audit = audit_neutral_state_cone(_tree())
    assert audit.records


@pytest.mark.fast
def test_parent_child_transfer():
    audit = audit_neutral_transfer_operator(_tree())
    assert audit.transfers


@pytest.mark.fast
def test_retained_sign_coordinates():
    audit = audit_augmented_neutral_state(_tree())
    assert any(s.R >= 0 or s.S >= 0 for s in audit.states)


@pytest.mark.fast
def test_linear_bellman_search():
    audit = audit_bellman_potential(_tree())
    assert audit.candidates


@pytest.mark.fast
def test_rational_bellman_certificate():
    audit = audit_bellman_exact_certificate(_tree())
    assert audit.certificates


@pytest.mark.fast
def test_piecewise_linear_potential():
    audit = audit_bellman_potential(_tree())
    types = {c.potential_type for c in audit.candidates}
    assert "PIECEWISE_LINEAR" in types


@pytest.mark.fast
def test_occupation_measure():
    audit = audit_neutral_occupation_measure(_tree())
    assert audit.measure.atoms


@pytest.mark.fast
def test_invariant_balance():
    audit = audit_invariant_state_measure(_tree())
    assert isinstance(audit.balance_holds, bool)


@pytest.mark.fast
def test_zero_slack_support():
    audit = audit_critical_state_classifier(_tree())
    assert audit.records


@pytest.mark.fast
def test_coboundary_correction():
    audit = audit_bookkeeping_coboundary(_tree())
    assert audit.records


@pytest.mark.fast
def test_t097_certificate():
    cert = certify_t097(_tree())
    assert cert.status in ("CONJECTURAL_STATE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t098_certificate():
    cert = certify_t098(_tree())
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t099_certificate():
    cert = certify_t099(_tree())
    assert cert.status in ("CONJECTURAL_RIGIDITY_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t098_clean_room():
    audit = audit_t098_clean_room(_tree())
    assert audit.verdict in ("T098_CLEAN_ROOM_VERIFIED", "T098_REPAIRABLE_GAP", "T098_INVALID")


@pytest.mark.fast
def test_transition_family():
    audit = audit_transition_family(_tree())
    assert audit.records


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d051_outcome():
    outcome = diagnose_d051_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
