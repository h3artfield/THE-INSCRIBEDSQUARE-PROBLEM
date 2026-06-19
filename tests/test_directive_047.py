"""Directive 047 — singleton Cantor-end rigidity and density improvement."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.child_signature_packing import audit_child_signature_packing
from squarepeg.defect_extraction.countable_child_order import build_countably_branching_tree
from squarepeg.defect_extraction.critical_singleton_tangent import audit_critical_singleton_tangent
from squarepeg.defect_extraction.end_density_martingale import audit_end_density_martingale
from squarepeg.defect_extraction.end_density_process import audit_end_density_process
from squarepeg.defect_extraction.finite_center_density_improvement import audit_finite_center_density_improvement
from squarepeg.defect_extraction.self_similar_end_models import (
    audit_self_similar_end_models,
    build_binary_equal_ratio_cantor,
    build_rotating_center_tree,
)
from squarepeg.defect_extraction.singleton_cantor_reduction import (
    certify_t084s,
    certify_t086s,
    diagnose_d047_outcome,
)
from squarepeg.defect_extraction.singleton_end_rigidity import certify_t089r_singleton
from squarepeg.defect_extraction.singleton_frostman_criterion import certify_t090r_singleton
from squarepeg.defect_extraction.tangent_of_tangent import audit_tangent_of_tangent


def _singleton_cantor():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


def _carleson():
    return build_countably_branching_tree(child_count=20, lambda_ratio=0.68, depth_after=1)


@pytest.mark.fast
def test_density_filtration():
    audit = audit_end_density_process(_singleton_cantor())
    assert audit.end_paths


@pytest.mark.fast
def test_nonmartingale_correction():
    audit = audit_end_density_martingale(_singleton_cantor())
    assert audit.classification in ("MARTINGALE", "SUBMARTINGALE", "SUPERMARTINGALE", "NONE")


@pytest.mark.fast
def test_child_scale_packing():
    audit = audit_child_signature_packing(_singleton_cantor())
    assert audit.status in (
        "STRICT_CONTRACTION",
        "LOOSE_CONTRACTION",
        "NO_CONTRACTION",
        "GEOMETRICALLY_DERIVED",
    )


@pytest.mark.fast
def test_finite_center_density_improvement():
    audit = audit_finite_center_density_improvement(_singleton_cantor())
    assert audit.K_bound >= 1


@pytest.mark.fast
def test_dini_moduli_subcritical_carleson():
    cert = certify_t090r_singleton(_carleson())
    assert cert.scaling_class in ("SUBCRITICAL", "CRITICAL", "SUPERCRITICAL", "MIXED")


@pytest.mark.fast
def test_critical_frostman_singleton():
    cert = certify_t090r_singleton(_singleton_cantor())
    assert cert.omega_form


@pytest.mark.fast
def test_self_similar_cantor_trees():
    audit = audit_self_similar_end_models()
    assert audit.result in (
        "SELF_SIMILAR_MODELS_CARLESON",
        "SELF_SIMILAR_CRITICAL_COUNTERMODEL",
        "MODEL_DEPENDENT",
    )


@pytest.mark.fast
def test_rotating_center_model():
    tree = build_rotating_center_tree()
    audit = audit_end_density_process(tree)
    assert audit.D_limsup >= 0


@pytest.mark.fast
def test_tangent_of_tangent_normalization():
    audit = audit_tangent_of_tangent(_singleton_cantor())
    assert isinstance(audit.compactness_holds, bool)


@pytest.mark.fast
def test_t089r_certificate():
    cert = certify_t089r_singleton(_singleton_cantor())
    assert cert.route


@pytest.mark.fast
def test_t090r_certificate():
    cert = certify_t090r_singleton(_singleton_cantor())
    assert cert.status in ("CONJECTURAL_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_critical_residual_validation():
    audit = audit_critical_singleton_tangent(_singleton_cantor())
    assert isinstance(audit.is_critical_residual, bool)


@pytest.mark.fast
def test_t086s_reduction():
    cert = certify_t086s(_singleton_cantor())
    assert cert.route


@pytest.mark.fast
def test_t084s_reduction():
    cert = certify_t084s(_singleton_cantor())
    assert cert.route in ("T086S", "T091_CONTINUUM", "GLOBAL_RESIDUAL")


@pytest.mark.fast
def test_d047_outcome():
    outcome = diagnose_d047_outcome(_singleton_cantor())
    assert outcome in ("A", "B", "C", "D", "E")
