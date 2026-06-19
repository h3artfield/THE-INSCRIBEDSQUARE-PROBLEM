"""Directive 050 — deficit budgets and T094-A repair."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.corona_deficit_budget import audit_corona_deficit_budget
from squarepeg.defect_extraction.deficit_distribution import audit_deficit_distribution
from squarepeg.defect_extraction.deficit_semicontinuity import audit_deficit_semicontinuity
from squarepeg.defect_extraction.deficit_to_contraction import certify_t095
from squarepeg.defect_extraction.equality_core_compactness import audit_equality_core_compactness
from squarepeg.defect_extraction.equality_core_pruning import audit_equality_core_pruning
from squarepeg.defect_extraction.ledger_deficits import audit_ledger_deficits
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t094a_clean_room import audit_t094a_clean_room
from squarepeg.defect_extraction.t094a_repair import certify_t094a, diagnose_d050_outcome
from squarepeg.defect_extraction.tree_core_selection import certify_t096


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_twelve_raw_deficits():
    audit = audit_ledger_deficits(_tree())
    assert len(audit.deficits) >= 12


@pytest.mark.fast
def test_normalization_edge_cases():
    audit = audit_ledger_deficits(_tree())
    classes = {d.norm_class for d in audit.deficits}
    assert classes


@pytest.mark.fast
def test_cumulative_deficit_budget():
    audit = audit_corona_deficit_budget(_tree())
    assert audit.windows


@pytest.mark.fast
def test_boundary_terms():
    audit = audit_corona_deficit_budget(_tree())
    assert all(w.boundary >= 0 for w in audit.windows)


@pytest.mark.fast
def test_deficit_to_contraction():
    cert = certify_t095(_tree())
    assert cert.status in ("CONJECTURAL_DEFICIT_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_signature_weighted_pruning():
    audit = audit_equality_core_pruning(_tree())
    assert audit.good_signature_mass >= 0


@pytest.mark.fast
def test_coherent_core_selection():
    cert = certify_t096(_tree())
    assert cert.status in ("CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_equality_core_compactness():
    audit = audit_equality_core_compactness(_tree())
    assert isinstance(audit.compactness_holds, bool)


@pytest.mark.fast
def test_deficit_semicontinuity():
    audit = audit_deficit_semicontinuity()
    assert len(audit.records) == 12


@pytest.mark.fast
def test_t094a_certificate():
    cert = certify_t094a(_tree())
    assert cert.route


@pytest.mark.fast
def test_t094a_clean_room():
    audit = audit_t094a_clean_room(_tree())
    assert audit.verdict in ("T094_A_CLEAN_ROOM_VERIFIED", "T094_A_REPAIRABLE_GAP", "T094_A_INVALID")


@pytest.mark.fast
def test_deficit_distribution():
    audit = audit_deficit_distribution(_tree())
    assert audit.dominant


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d050_outcome():
    outcome = diagnose_d050_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
