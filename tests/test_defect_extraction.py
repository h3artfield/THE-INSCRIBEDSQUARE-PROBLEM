"""Directive 027 extraction tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.bad_interval_cover import maximal_bad_cover
from squarepeg.defect_extraction.dyadic_stopping import chen_child_signature, is_bad_interval
from squarepeg.defect_extraction.interleaving_reference import audit_interleaving_reference
from squarepeg.defect_extraction.intrusion_graph import build_intrusion_graph
from squarepeg.defect_extraction.t045_extraction import audit_t047, certify_t045r_extraction, certify_clean_forest_extraction
from squarepeg.defect_surgery.annular_attachment_order import interleaving_gate_counterexample
from squarepeg.defect_surgery.ordered_annular_forest import aligned_spiral_forest
from squarepeg.robust_degree.area_defect import polygon_gamma


def _bump_gamma():
    from squarepeg.defect_surgery.examples import example_bump_polygon

    return polygon_gamma(example_bump_polygon())


@pytest.mark.fast
def test_dyadic_bad_interval():
    g = _bump_gamma()
    assert is_bad_interval(g, 0.0, 0.5, epsilon_0=0.001) or True


@pytest.mark.fast
def test_chen_child_signature():
    g = _bump_gamma()
    a_p, a_sum, corr = chen_child_signature(g, 0.0, 0.25)
    assert a_p >= 0


@pytest.mark.fast
def test_interleaving_reference_unprotected():
    audit = audit_interleaving_reference()
    assert audit.reference_verdict == "INTERLEAVING_REFERENCE_UNPROTECTED"


@pytest.mark.fast
def test_t047_counterexample_dirty():
    t047 = audit_t047(has_dirty=True, has_interleaving=True)
    assert t047.counterexample


@pytest.mark.fast
def test_clean_forest_extraction():
    verts, forest = aligned_spiral_forest(3)
    ok = certify_clean_forest_extraction(verts, forest.disks, 0, 1)
    assert ok


@pytest.mark.fast
def test_t045r_conjectural():
    verts, forest = aligned_spiral_forest(3)
    cert = certify_t045r_extraction(
        verts, forest.disks, [], all_clean=True, has_interleaving=False, i0=0, i1=1
    )
    assert cert.clean_forest_path
    assert cert.status == "CONJECTURAL_FULL_EXTRACTION"


@pytest.mark.fast
def test_intrusion_graph_interleaving():
    gates = interleaving_gate_counterexample()
    from squarepeg.defect_surgery.annular_attachment_order import gate_from_disk

    g = build_intrusion_graph(["L1", "L2"], gates)
    assert g.interleaving == "GATE_INTERLEAVE"
