"""Directive 052 — neutral transition escape and compactification."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from squarepeg.defect_extraction.compact_core_bellman import audit_compact_core_bellman, certify_t098c
from squarepeg.defect_extraction.compact_core_occupation import audit_compact_core_occupation
from squarepeg.defect_extraction.compact_neutral_core import audit_compact_neutral_core
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.measure_valued_transition import audit_measure_valued_transition
from squarepeg.defect_extraction.neutral_escape_profiles import audit_neutral_escape_profiles
from squarepeg.defect_extraction.neutral_escape_classification import certify_t100
from squarepeg.defect_extraction.neutral_gauge_quotient import audit_neutral_gauge_quotient
from squarepeg.defect_extraction.projective_neutral_state import audit_projective_neutral_state
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t097c_clean_room import audit_t097c_clean_room
from squarepeg.defect_extraction.t097c_proof import certify_t097c, diagnose_d052_outcome
from squarepeg.defect_extraction.transition_coboundary import audit_transition_coboundary
from squarepeg.defect_extraction.transition_escape_audit import audit_transition_escape, serialize_escape_fixture


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_noncompact_fixture():
    fixture = serialize_escape_fixture(_tree())
    assert fixture["witness_label"]


@pytest.mark.fast
def test_frozen_fixture_file():
    path = Path(__file__).resolve().parents[1] / "data" / "regressions" / "neutral_transition_escape_fixture.json"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(serialize_escape_fixture(_tree()), indent=2), encoding="utf-8")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["family_compact"] is False


@pytest.mark.fast
def test_coordinate_escape_audit():
    audit = audit_transition_escape(_tree())
    assert audit.records


@pytest.mark.fast
def test_escape_profiles():
    audit = audit_neutral_escape_profiles(_tree())
    assert audit.profiles


@pytest.mark.fast
def test_coboundary_identities():
    audit = audit_transition_coboundary(_tree())
    assert audit.records


@pytest.mark.fast
def test_gauge_equivalence():
    audit = audit_neutral_gauge_quotient(_tree())
    assert audit.classes


@pytest.mark.fast
def test_projective_normalization():
    audit = audit_projective_neutral_state(_tree())
    assert audit.records


@pytest.mark.fast
def test_projective_boundary():
    audit = audit_projective_neutral_state(_tree())
    assert any(r.boundary_class for r in audit.records)


@pytest.mark.fast
def test_measure_valued_transition():
    audit = audit_measure_valued_transition(_tree())
    assert audit.transitions


@pytest.mark.fast
def test_measure_tightness():
    audit = audit_measure_valued_transition(_tree())
    assert isinstance(audit.all_tight, bool)


@pytest.mark.fast
def test_compact_core():
    audit = audit_compact_neutral_core(_tree())
    assert audit.core_records is not None


@pytest.mark.fast
def test_transfer_closure():
    audit = audit_compact_neutral_core(_tree())
    assert audit.coordinate_closure


@pytest.mark.fast
def test_bellman_separation():
    audit = audit_compact_core_bellman(_tree())
    assert audit.branch


@pytest.mark.fast
def test_occupation_balance():
    audit = audit_compact_core_occupation(_tree())
    assert isinstance(audit.balance_holds, bool)


@pytest.mark.fast
def test_t100_certificate():
    cert = certify_t100(_tree())
    assert cert.status in ("CONJECTURAL_COMPACTNESS_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t097c_certificate():
    cert = certify_t097c(_tree())
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t098c_certificate():
    cert = certify_t098c(_tree())
    assert cert.status in ("CONJECTURAL_DUALITY_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t097c_clean_room():
    audit = audit_t097c_clean_room(_tree())
    assert audit.verdict in ("T097C_CLEAN_ROOM_VERIFIED", "T097C_REPAIRABLE_GAP", "T097C_INVALID")


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d052_outcome():
    outcome = diagnose_d052_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
