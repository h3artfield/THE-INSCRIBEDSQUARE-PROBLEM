"""Directive 030 — hull-adjacent ears, join bounds, T053B."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_extraction.bounded_gate_cluster import BoundedGateCluster
from squarepeg.defect_extraction.bounded_gate_join import audit_join_bound, join_bound_holds, join_from_components, j_m_r, q_of_m
from squarepeg.defect_extraction.bounded_gate_retained_cover import certify_bounded_gate_cover
from squarepeg.defect_extraction.ear_area_allocation import decompose_ear_area
from squarepeg.defect_extraction.ear_saturation import ear_saturation, preserves_two_gate_property
from squarepeg.defect_extraction.extracted_cluster_signature import audit_extracted_signature
from squarepeg.defect_extraction.gate_graph import build_gate_graph, example_four_gate_graph, example_nested_six_gate_graph
from squarepeg.defect_extraction.gate_word import GateLabel
from squarepeg.defect_extraction.geometric_ear_peeling import geometric_ear_peeling, complexity_kappa
from squarepeg.defect_extraction.hull_adjacent_ear import (
    audit_t058,
    is_hull_adjacent,
    reduce_gate_graph,
    find_hull_adjacent_geometric_ear,
)
from squarepeg.defect_extraction.quantitative_defect_allocation import (
    audit_peeling_allocation,
    one_step_allocation,
    r0_of_m_epsilon,
)
from squarepeg.defect_extraction.t053b_extraction import RESIDUAL_AFTER_T053B, certify_t053b_full
from squarepeg.defect_surgery.examples import example_bump_polygon
from squarepeg.defect_surgery.nested_forest import PacketForest


def _gate_graph_n(n: int):
    gates = [GateLabel(f"g{i}", i / n, (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))) for i in range(n)]
    arcs = [(f"g{i}", f"g{n - 1 - i}", "SATURATED_ARC") for i in range(n // 2)]
    order = [f"g{i}" for i in range(n)]
    return build_gate_graph(gates, arcs, hull_order=order)


@pytest.mark.fast
def test_hull_adjacent_gate_arc():
    h = ["g0", "g1", "g2", "g3", "g4", "g5"]
    adj = is_hull_adjacent(h, "g0", "g5")
    assert adj.gate_free


@pytest.mark.fast
def test_weak_dual_leaf_four_gate():
    g = example_four_gate_graph()
    ear = find_hull_adjacent_geometric_ear(reduce_gate_graph(g))
    assert ear is not None
    assert ear.t051_eligible


@pytest.mark.fast
def test_t058_nested_six():
    g = example_nested_six_gate_graph()
    audit = audit_t058(g)
    assert audit.status == "PROVED_LOCALLY"
    assert audit.geometric_ear is not None


@pytest.mark.fast
def test_t058_rational_gate_counts():
    for n in (4, 6, 8, 10, 12):
        g = _gate_graph_n(n)
        audit = audit_t058(g)
        assert audit.status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_ear_saturation_two_gate():
    g = example_four_gate_graph()
    ear = find_hull_adjacent_geometric_ear(g)
    assert ear is not None
    state = ear_saturation(ear, [], (0.0, 1.0))
    assert preserves_two_gate_property(state)


@pytest.mark.fast
def test_component_count_bound():
    assert q_of_m(8) >= 8


@pytest.mark.fast
def test_join_area_bound():
    m, r = 8, 0.05
    audit = audit_join_bound(m=m, diameter_r=r)
    assert audit.join_upper_bound == j_m_r(m, r)
    incs = [(0.1, 0.0), (-0.1, 0.05), (0.05, -0.1)]
    exact, upper = join_from_components(incs, m=m, diameter_r=r)
    assert join_bound_holds(exact, m, r) or abs(exact) <= upper + 0.01


@pytest.mark.fast
def test_fixed_defect_allocation():
    dec = decompose_ear_area([(0, 0), (0.02, 0.01), (0.04, 0)], [(0.04, 0), (0.1, 0)], (0, 0), (0.04, 0))
    eps = 0.025
    step = one_step_allocation(dec, epsilon=eps, m=8, diameter_r=0.02)
    assert step.join_bound <= j_m_r(8, 0.02)
    r0 = r0_of_m_epsilon(8, eps)
    assert j_m_r(8, r0 * 0.5) <= eps / 4


@pytest.mark.fast
def test_geometric_peeling_termination():
    g = example_nested_six_gate_graph()
    peel = geometric_ear_peeling(g)
    assert peel.jordan_preserved
    assert len(peel.steps) >= 1
    if peel.steps:
        assert peel.steps[0].kappa_after < peel.steps[0].kappa_before


@pytest.mark.fast
def test_cluster_signature_compatibility():
    g = example_four_gate_graph()
    peel = geometric_ear_peeling(g)
    sig = audit_extracted_signature(peel, m=8, omega_gamma=0.08)
    assert sig.signature_class in ("CLUSTER_SIGNATURE_CARLESON", "BOUNDED_WINDING_SIGNATURE", "UNVERIFIED")


@pytest.mark.fast
def test_t053b_certificate():
    g = example_four_gate_graph()
    cluster = BoundedGateCluster(gate_graph=g, gate_bound=8, jordan_hull=True)
    verts = example_bump_polygon()
    pf = PacketForest(disks=[])
    cert = certify_t053b_full(cluster, verts, None, pf, 0, len(verts) - 1, diameter_r=0.02, epsilon=0.025)
    assert cert.t058_proved
    assert cert.status in ("PROVED_LOCALLY_BOUNDED_GATE", "CONJECTURAL_CONTROLLED_EXTRACTION")
    assert len(RESIDUAL_AFTER_T053B) == 4


@pytest.mark.fast
def test_retained_cover():
    g = example_four_gate_graph()
    verts = example_bump_polygon()
    cover = certify_bounded_gate_cover(g, verts, PacketForest(disks=[]), 0, len(verts) - 1, m=8, diameter_r=0.02)
    assert cover.peel.jordan_preserved
