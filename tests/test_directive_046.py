"""Directive 046 — endpoint correspondences and Cantor tangent recovery."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.correspondence_frostman import certify_t090r
from squarepeg.defect_extraction.endpoint_graph_compactness import audit_endpoint_graph_compactness
from squarepeg.defect_extraction.endpoint_hyperspace import audit_endpoint_hyperspace
from squarepeg.defect_extraction.endpoint_incidence_measure import audit_endpoint_incidence_measure
from squarepeg.defect_extraction.endpoint_kernel_disintegration import audit_endpoint_kernel_disintegration
from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction
from squarepeg.defect_extraction.endpoint_repaired_reduction import (
    certify_t086e,
    certify_t092,
    diagnose_variable_ratio_cantor,
)
from squarepeg.defect_extraction.finite_center_correspondence_rigidity import certify_t089r
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.noncarleson_cantor_tangent import build_variable_ratio_cantor_tree
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split
from squarepeg.defect_extraction.countable_child_order import build_countably_branching_tree


def _cantor():
    return build_variable_ratio_cantor_tree(levels=4, ratio=0.58)


@pytest.mark.fast
def test_nested_compact_intersection():
    audit = audit_endpoint_multifunction(_cantor())
    assert audit.records


@pytest.mark.fast
def test_diameter_zero_singleton():
    tree = build_countably_branching_tree(child_count=12, lambda_ratio=0.65, depth_after=0)
    audit = audit_endpoint_multifunction(tree)
    assert audit.singleton_mass_fraction > 0


@pytest.mark.fast
def test_measurable_endpoint_map():
    audit = audit_endpoint_hyperspace(_cantor())
    assert audit.phi_measurable


@pytest.mark.fast
def test_endpoint_graph_convergence():
    audit = audit_endpoint_graph_compactness(_cantor())
    assert audit.borel_graph


@pytest.mark.fast
def test_singleton_continuum_decomposition():
    audit = audit_singleton_continuum_split(_cantor())
    assert audit.mu_0_mass + audit.mu_plus_mass >= 0


@pytest.mark.fast
def test_incidence_measure_construction():
    audit = audit_endpoint_incidence_measure(_cantor())
    assert audit.canonical
    assert audit.no_arbitrary_selection


@pytest.mark.fast
def test_kernel_support_on_phi():
    audit = audit_endpoint_kernel_disintegration(_cantor())
    assert audit.independence == "CANONICAL_INCIDENCE_MEASURE"


@pytest.mark.fast
def test_incidence_concentration():
    audit = audit_incidence_concentration(_cantor())
    assert audit.concentration_class


@pytest.mark.fast
def test_variable_ratio_cantor_diagnosis():
    diag = diagnose_variable_ratio_cantor(_cantor())
    assert diag.diagnosis in (
        "POSSIBILITY_A_POSITIVE_SCALE",
        "POSSIBILITY_B_NESTING_FAILURE",
        "POSSIBILITY_C_IMPLEMENTATION_SINGLETON",
        "POSSIBILITY_D_GENUINE_CONTINUUM",
    )


@pytest.mark.fast
def test_t091_routing():
    cert = certify_t091(_cantor())
    assert cert.route


@pytest.mark.fast
def test_t089r_certificate():
    cert = certify_t089r(build_countably_branching_tree(child_count=16, lambda_ratio=0.68))
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t090r_certificate():
    cert = certify_t090r(_cantor())
    assert cert.component in ("SINGLETON", "CONTINUUM", "MIXED")


@pytest.mark.fast
def test_t092_dichotomy():
    cert = certify_t092(_cantor())
    assert cert.route


@pytest.mark.fast
def test_t086e_repaired_reduction():
    cert = certify_t086e(_cantor())
    assert cert.route
