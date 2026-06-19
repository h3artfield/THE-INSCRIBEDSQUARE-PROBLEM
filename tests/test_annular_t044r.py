"""Directive 026 annular bridge tests."""

from __future__ import annotations

import math
import pytest

from squarepeg.defect_surgery.annular_attachment_order import (
    current_annular_class_verdict,
    interleaving_gate_counterexample,
    is_gate_ordered,
    ordered_gate_example,
)
from squarepeg.defect_surgery.angular_monotonicity import audit_angular_monotone
from squarepeg.defect_surgery.center_coherence import audit_center_coherence
from squarepeg.defect_surgery.ordered_annular_forest import (
    aligned_spiral_forest,
    audit_ordered_annular_forest,
    gates_from_forest,
)
from squarepeg.defect_surgery.attachment_chain_simplicity import build_annular_attachment_chain
from squarepeg.defect_surgery.exact_component_decomposition import PathComponent, component_delta, master_area_identity
from squarepeg.defect_surgery.annular_winding_bound import audit_annular_winding
from squarepeg.defect_surgery.complete_defect_cover import audit_complete_defect_cover, cover_implies_beta_vanishing
from squarepeg.defect_surgery.t046_signature_theorem import certify_t046, run_t046_clean_room
from squarepeg.defect_surgery.t044r_annular_bridge import certify_t044r, classify_scale_branch
from squarepeg.defect_surgery.attachment_chain import attachment_chain_area, AttachmentChain


@pytest.mark.fast
def test_current_annular_insufficient():
    assert current_annular_class_verdict() == "CURRENT_ANNULAR_CLASS_INSUFFICIENT"


@pytest.mark.fast
def test_interleaving_not_gate_ordered():
    gates = interleaving_gate_counterexample()
    assert not is_gate_ordered(gates)


@pytest.mark.fast
def test_ordered_gates_pass():
    gates = ordered_gate_example(n=4)
    assert is_gate_ordered(gates)
    assert audit_angular_monotone(gates).passes
    assert audit_center_coherence(gates).passes


@pytest.mark.fast
def test_interleaving_macroscopic_sigma():
    from squarepeg.defect_surgery.annular_attachment_order import interleaving_attachment_components

    comps = interleaving_attachment_components()
    pts = build_annular_attachment_chain(comps)
    ident = master_area_identity(comps)
    assert ident.exact
    assert abs(ident.attachment_chain_area) > 0.05


@pytest.mark.fast
def test_aligned_spiral_ordered():
    verts, forest = aligned_spiral_forest(n_levels=4)
    gates = gates_from_forest(verts, forest)
    audit = audit_ordered_annular_forest(gates, require_angular=False)
    assert audit.gate_ordered


@pytest.mark.fast
def test_t046_aligned_spiral():
    verts, forest = aligned_spiral_forest(n_levels=3)
    cert = certify_t046(verts, forest, 0, 1, omega_gamma=0.08, complete_cover=True)
    assert cert.ordered_audit.gate_ordered
    assert cert.ordered_audit.satisfies_ordered_class
    assert cert.status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_complete_defect_cover_noncircular():
    verts, forest = aligned_spiral_forest(n_levels=3)
    cover = audit_complete_defect_cover(verts, forest, 0, len(verts) - 1, delta=0.1)
    assert cover.noncircular


@pytest.mark.fast
def test_t046_clean_room():
    assert run_t046_clean_room().verdict == "T046_CLEAN_ROOM_VERIFIED"


@pytest.mark.fast
def test_t044r_shrinking_branch():
    verts, forest = aligned_spiral_forest(n_levels=3)
    cert = certify_t044r(verts, forest, 0, 1, diameters=[0.01, 0.006, 0.004])
    assert cert.branch == "SHRINKING_SCALE"
    assert cert.status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_t044r_positive_branch():
    assert classify_scale_branch([0.05, 0.04]) == "POSITIVE_SCALE"
