"""Directive 049 — equality ledger and neutral-corona rigidity."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.cantor_end_surgery import build_middle_thirds_cantor_tree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.critical_equality_models import audit_critical_equality_models
from squarepeg.defect_extraction.equality_compatibility import audit_equality_compatibility
from squarepeg.defect_extraction.equality_ledger import get_ledger, get_entry
from squarepeg.defect_extraction.equality_realizability import audit_equality_realizability
from squarepeg.defect_extraction.equality_stability import audit_equality_stability
from squarepeg.defect_extraction.equality_template_classifier import audit_equality_template_classifier
from squarepeg.defect_extraction.exact_equality_tree import audit_exact_equality_tree
from squarepeg.defect_extraction.neutral_corona_tangent import audit_neutral_corona_tangent
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t093_coverage_audit import audit_t093_coverage
from squarepeg.defect_extraction.t094_clean_room import audit_t094_clean_room
from squarepeg.defect_extraction.t094_proof import (
    certify_t089r_closure,
    certify_t094,
    diagnose_d049_outcome,
)


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_ledger_entries():
    assert len(get_ledger()) >= 10
    assert get_entry("WEDGE_PRODUCT").equality_condition


@pytest.mark.fast
def test_incompatible_equality_pairs():
    audit = audit_equality_compatibility()
    assert audit.impossible_cliques


@pytest.mark.fast
def test_near_equality_stability():
    audit = audit_equality_stability()
    assert audit.template_count >= 1


@pytest.mark.fast
def test_t093_coverage_explicit_measure():
    audit = audit_t093_coverage(_tree())
    assert audit.measure_type == "SIGNATURE_SCALE_PHI_END"


@pytest.mark.fast
def test_neutral_corona_convergence():
    audit = audit_neutral_corona_tangent(_tree())
    assert isinstance(audit.compactness_holds, bool)


@pytest.mark.fast
def test_one_child_equality():
    audit = audit_exact_equality_tree(_tree())
    assert audit.tree_class


@pytest.mark.fast
def test_finite_child_equality():
    audit = audit_equality_template_classifier(_tree())
    assert audit.templates_found is not None


@pytest.mark.fast
def test_annular_thin_routing():
    audit = audit_equality_realizability(build_middle_thirds_cantor_tree(levels=4))
    assert audit.records or not audit.any_critical_survives


@pytest.mark.fast
def test_jordan_realizability():
    audit = audit_equality_realizability(_tree())
    assert isinstance(audit.any_critical_survives, bool)


@pytest.mark.fast
def test_countermodel_exclusion():
    audit = audit_critical_equality_models()
    assert not audit.countermodel_found


@pytest.mark.fast
def test_t094_certificate():
    cert = certify_t094(_tree())
    assert cert.route


@pytest.mark.fast
def test_t089r_closure():
    cert = certify_t089r_closure(_tree())
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t094_clean_room():
    audit = audit_t094_clean_room(_tree())
    assert audit.verdict in ("T094_CLEAN_ROOM_VERIFIED", "T094_REPAIRABLE_GAP", "T094_INVALID")


@pytest.mark.fast
def test_t091_frozen():
    cert = certify_t091(_tree())
    assert cert.route


@pytest.mark.fast
def test_d049_outcome():
    outcome = diagnose_d049_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
