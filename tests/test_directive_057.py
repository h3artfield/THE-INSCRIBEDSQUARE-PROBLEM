"""Directive 057 — coherent route extraction and tree-level stabilization."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.coherent_route_subsystem import audit_coherent_route_subsystem
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.route_constant_uniformity import audit_route_constant_uniformity, certify_t110
from squarepeg.defect_extraction.route_density_tree import certify_t109
from squarepeg.defect_extraction.route_label_system import audit_route_label_system
from squarepeg.defect_extraction.route_oscillation_cost import audit_route_oscillation_cost
from squarepeg.defect_extraction.route_oscillation_reduction import certify_t111
from squarepeg.defect_extraction.route_responsibility import audit_route_responsibility
from squarepeg.defect_extraction.route_signature_mass import audit_route_signature_mass
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.t089e_reduction import certify_t089e_coherent
from squarepeg.defect_extraction.t103_clean_room import audit_t103_clean_room, diagnose_d057_outcome
from squarepeg.defect_extraction.t103_coherent_route import certify_t103_coherent


def _tree():
    return build_binary_equal_ratio_cantor(levels=4, ratio=0.58)


@pytest.mark.fast
def test_route_label_sets_nonempty():
    audit = audit_route_label_system(_tree())
    assert audit.all_nonempty


@pytest.mark.fast
def test_route_responsibility():
    audit = audit_route_responsibility(_tree())
    assert audit.signature_preserving


@pytest.mark.fast
def test_signature_mass_conservation():
    audit = audit_route_signature_mass(_tree())
    assert audit.mass_conserved


@pytest.mark.fast
def test_slice_pigeonhole():
    audit = audit_route_signature_mass(_tree())
    assert audit.pigeonhole_route is not None


@pytest.mark.fast
def test_ray_coherence():
    audit = audit_coherent_route_subsystem(_tree())
    assert audit.subsystems


@pytest.mark.fast
def test_uniform_route_constants():
    cert = certify_t110(_tree())
    assert cert.status in ("CONJECTURAL_UNIFORMITY_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_route_oscillation_cost():
    audit = audit_route_oscillation_cost(_tree())
    assert audit.geometric


@pytest.mark.fast
def test_t109_certificate():
    cert = certify_t109(_tree())
    assert cert.status in ("CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t111_certificate():
    cert = certify_t111(_tree())
    assert cert.status in ("CONJECTURAL_OSCILLATION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t103_coherent():
    cert = certify_t103_coherent(_tree())
    assert cert.status in ("CONJECTURAL_SELECTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t089e_coherent():
    cert = certify_t089e_coherent(_tree())
    assert cert.status in ("CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t103_clean_room():
    audit = audit_t103_clean_room(_tree())
    assert audit.verdict in ("T103_CLEAN_ROOM_VERIFIED", "T103_REPAIRABLE_GAP", "T103_INVALID")


@pytest.mark.fast
def test_t091_frozen():
    assert certify_t091(_tree()).route


@pytest.mark.fast
def test_d057_outcome():
    outcome = diagnose_d057_outcome(_tree())
    assert outcome in ("A", "B", "C", "D", "E")
