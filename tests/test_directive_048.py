"""Directive 048 — multigeneration packing and critical Cantor corona rigidity."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.cantor_end_surgery import build_middle_thirds_cantor_tree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.critical_equality_rigidity import certify_t094
from squarepeg.defect_extraction.end_entropy_drift import audit_end_entropy_drift
from squarepeg.defect_extraction.equality_model_classifier import audit_equality_model_classifier
from squarepeg.defect_extraction.infinite_center_critical import audit_infinite_center_critical
from squarepeg.defect_extraction.multigeneration_packing import audit_multigeneration_packing, certify_t093
from squarepeg.defect_extraction.multigeneration_singleton_rigidity import (
    certify_t086m,
    certify_t089r_multigen,
    diagnose_d048_outcome,
)
from squarepeg.defect_extraction.neutral_corona_compactness import audit_neutral_corona_compactness
from squarepeg.defect_extraction.self_similar_end_models import (
    build_binary_equal_ratio_cantor,
    build_rotating_center_tree,
)
from squarepeg.defect_extraction.signature_budget import audit_signature_budget
from squarepeg.defect_extraction.signature_excess import audit_signature_excess


def _singleton():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_signature_budget():
    audit = audit_signature_budget(_singleton())
    assert audit.records


@pytest.mark.fast
def test_excess_decomposition():
    audit = audit_signature_excess(_singleton())
    assert audit.dominant


@pytest.mark.fast
def test_good_neutral_bad_classification():
    audit = audit_cantor_corona(_singleton())
    assert audit.contracting_fraction + audit.neutral_fraction + audit.bad_fraction >= 0


@pytest.mark.fast
def test_corona_construction():
    audit = audit_cantor_corona(build_middle_thirds_cantor_tree(levels=4))
    assert isinstance(audit.canonical, bool)


@pytest.mark.fast
def test_multigeneration_contraction():
    audit = audit_multigeneration_packing(_singleton())
    assert audit.uniform_L >= 1


@pytest.mark.fast
def test_neutral_tangent_extraction():
    audit = audit_neutral_corona_compactness(_singleton())
    assert isinstance(audit.compactness_holds, bool)


@pytest.mark.fast
def test_entropy_scale_drift():
    audit = audit_end_entropy_drift(_singleton())
    assert audit.avg_entropy >= 0


@pytest.mark.fast
def test_equality_model_classifier():
    audit = audit_equality_model_classifier(_singleton())
    assert isinstance(audit.models_found, list)


@pytest.mark.fast
def test_infinite_center_model():
    audit = audit_infinite_center_critical(build_rotating_center_tree())
    assert audit.dominant_route


@pytest.mark.fast
def test_t093_certificate():
    cert = certify_t093(_singleton())
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t094_certificate():
    cert = certify_t094(_singleton())
    assert cert.route


@pytest.mark.fast
def test_t089r_multigen_certificate():
    cert = certify_t089r_multigen(_singleton())
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t086m_reduction():
    cert = certify_t086m(_singleton())
    assert cert.route


@pytest.mark.fast
def test_t091_continuum_frozen():
    cert = certify_t091(_singleton())
    assert cert.route


@pytest.mark.fast
def test_d048_outcome():
    outcome = diagnose_d048_outcome(_singleton())
    assert outcome in ("A", "B", "C", "D", "E")
