"""Directive 029 — gate word, graph, outerplanarity, ears, extraction."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.block_decomposition import decompose_blocks
from squarepeg.defect_extraction.bounded_gate_cluster import BoundedGateCluster, audit_t057
from squarepeg.defect_extraction.ear_area_allocation import audit_defect_allocation, decompose_ear_area
from squarepeg.defect_extraction.ear_peeling import peel_ears
from squarepeg.defect_extraction.finite_intrusion_extraction import audit_t050r, certify_t053b
from squarepeg.defect_extraction.gate_accumulation import audit_gate_accumulation, example_unbounded_gate_sequence
from squarepeg.defect_extraction.gate_graph import example_four_gate_graph, example_nested_six_gate_graph
from squarepeg.defect_extraction.gate_word import GateLabel, build_gate_word, hull_vs_parameter_interleaves
from squarepeg.defect_extraction.geometric_ear import audit_t056, ear_removal_confluence
from squarepeg.defect_extraction.nonjordan_hull import classify_hull
from squarepeg.defect_extraction.outerplanar_structure import audit_outerplanarity
from squarepeg.defect_extraction.cluster_forest import build_cluster_forest


@pytest.mark.fast
def test_gate_word_construction():
    gates = [GateLabel(f"g{i}", i / 4.0, (float(i), 0.0)) for i in range(4)]
    word = build_gate_word(gates, hull_order=["g0", "g1", "g2", "g3"])
    assert word.parameter_order[0] == "g0"
    assert word.pairing_kind in ("ADJACENT", "NESTED", "MIXED")


@pytest.mark.fast
def test_hull_vs_parameter_order():
    gates = [GateLabel(f"g{i}", i / 4.0, (float(i), 0.0)) for i in range(4)]
    word = build_gate_word(
        gates,
        hull_order=["g0", "g2", "g1", "g3"],
        param_order=["g0", "g1", "g2", "g3"],
        pairings=[("g0", "g1"), ("g2", "g3")],
    )
    assert word.hull_boundary_order != word.parameter_order


@pytest.mark.fast
def test_outerplanarity_four_gate():
    g = example_four_gate_graph()
    audit = audit_outerplanarity(g)
    assert audit.is_outerplanar
    assert audit.status == "PROVED_LOCALLY_NONCROSSING"


@pytest.mark.fast
def test_block_decomposition():
    g = example_four_gate_graph()
    decomp = decompose_blocks(g)
    assert len(decomp.blocks) >= 1
    assert len(decomp.leaf_blocks) >= 1


@pytest.mark.fast
def test_graph_ear_vs_geometric_ear():
    g = example_four_gate_graph()
    decomp = decompose_blocks(g)
    t056 = audit_t056(g, decomp)
    assert t056.graph_ears
    assert t056.status == "PROVED_LOCALLY_GRAPH_EAR"


@pytest.mark.fast
def test_ear_removal_confluence():
    assert ear_removal_confluence() == "EAR_REMOVAL_ORDER_DEPENDENT_BUT_TERMINATING"


@pytest.mark.fast
def test_ear_peeling_four_gate():
    g = example_four_gate_graph()
    result = peel_ears(g)
    assert result.status in ("TWO_GATE_REMAINDER", "ALL_EARS_SURGERY")
    assert result.jordan_preserved


@pytest.mark.fast
def test_ear_peeling_nested_six():
    g = example_nested_six_gate_graph()
    result = peel_ears(g)
    assert len(result.steps) >= 1


@pytest.mark.fast
def test_exact_area_allocation():
    ear = [(0, 0), (0.5, 0.5), (1, 0)]
    rem = [(1, 0), (1, 1), (0, 1), (0, 0)]
    dec = decompose_ear_area(ear, rem, (0, 0), (1, 0))
    assert dec.area_join is not None
    assert dec.area_ear + dec.area_remainder + dec.area_join == pytest.approx(dec.area_total, rel=1e-3)


@pytest.mark.fast
def test_join_signature_concentration():
    dec = decompose_ear_area([(0, 0), (0.01, 0.01), (1, 0)], [(1, 0), (2, 0)], (0, 0), (1, 0))
    audit = audit_defect_allocation(dec, epsilon=0.001, gate_count=6)
    assert audit.outcome in ("EAR_CARRIES_DEFECT", "JOIN_CARRIES_DEFECT", "REMAINDER_FRACTION", "UNRESOLVED")


@pytest.mark.fast
def test_bounded_gate_reduction():
    g = example_four_gate_graph()
    cluster = BoundedGateCluster(gate_graph=g, gate_bound=8, jordan_hull=True)
    t057 = audit_t057(cluster)
    assert t057.outcome == "TWO_GATE_FOREST"
    assert t057.status == "PROVED_LOCALLY_BOUNDED"


@pytest.mark.fast
def test_unbounded_gate_sequence():
    recs = example_unbounded_gate_sequence(12)
    audit = audit_gate_accumulation(recs)
    assert audit.unbounded
    assert audit.residual_class != "NONE"


@pytest.mark.fast
def test_nonjordan_hull_classification():
    audit = classify_hull(is_jordan_disk=False, simply_connected=True, pinch_points=1)
    assert "PINCHED_BOUNDARY" in audit.obstructions


@pytest.mark.fast
def test_t050r_classification():
    r = audit_t050r(gate_count=6, jordan_hull=True, outerplanar=True, unbounded_sequence=False, positive_scale=False)
    assert r.branch == "OUTERPLANAR_MULTI_GATE"


@pytest.mark.fast
def test_t053b_certificate():
    g = example_four_gate_graph()
    cluster = BoundedGateCluster(gate_graph=g, gate_bound=8, jordan_hull=True)
    forest = build_cluster_forest([])
    cert = certify_t053b(cluster, [], forest, 0, 1)
    assert cert.t057.outcome == "TWO_GATE_FOREST"
    assert cert.status in ("CONJECTURAL_CONTROLLED_EXTRACTION", "PROVED_LOCALLY_BOUNDED_GATE")


@pytest.mark.fast
def test_interleaving_unprotected():
    gates = [GateLabel(f"g{i}", i / 4.0, (float(i), 0.0)) for i in range(4)]
    word = build_gate_word(
        gates,
        pairings=[("g0", "g3"), ("g1", "g2")],
        param_order=["g0", "g1", "g2", "g3"],
    )
    assert word.pairing_kind in ("NESTED", "MIXED", "SEPARATED", "ALTERNATING")
    assert not hull_vs_parameter_interleaves(word) or word.pairing_kind != "ALTERNATING"
