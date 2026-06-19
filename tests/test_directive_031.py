"""Directive 031 — sparse/dense gate dichotomy."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_extraction.controlled_dense_class import (
    certify_finite_center_dense,
    certify_ordered_diffuse,
)
from squarepeg.defect_extraction.dense_attachment_signature import audit_dense_signature, winding_amplification
from squarepeg.defect_extraction.dense_gate_trichotomy import DenseGateRecord, audit_dense_gate_trichotomy
from squarepeg.defect_extraction.diffuse_gate_limit import classify_diffuse_limit
from squarepeg.defect_extraction.gate_block_decomposition import partition_gate_blocks
from squarepeg.defect_extraction.gate_concentration import extract_concentrated_subblock
from squarepeg.defect_extraction.gate_density import (
    C0,
    C1,
    classify_gate_density,
    gate_complexity,
    join_bound_from_lambda_mr,
    join_bound_from_lambda_q,
    sparse_sequence,
)
from squarepeg.defect_extraction.gate_graph import example_four_gate_graph
from squarepeg.defect_extraction.gate_word_limit import classify_gate_word
from squarepeg.defect_extraction.normalized_gate_measure import (
    NormalizedGate,
    gate_spacing_normalized,
    normalize_hull,
)
from squarepeg.defect_extraction.sparse_gate_extraction import certify_t060, join_vanishes
from squarepeg.defect_surgery.examples import example_bump_polygon


@pytest.mark.fast
def test_lambda_mr_complexity():
    gc = gate_complexity(100, 0.0005)
    assert gc.lambda_mr == pytest.approx(0.05)
    assert join_bound_from_lambda_mr(gc.lambda_mr) == pytest.approx(C1 * gc.lambda_mr ** 2)


@pytest.mark.fast
def test_lambda_q_sharper_bound():
    lam_q = 0.03
    assert join_bound_from_lambda_q(lam_q) == pytest.approx(C0 * lam_q ** 2)


@pytest.mark.fast
def test_sparse_join_convergence():
    lambdas = [0.008, 0.005, 0.003, 0.001]
    assert sparse_sequence(lambdas)
    assert join_vanishes(lambdas)


@pytest.mark.fast
def test_sparse_defect_allocation_no_vanishing_fraction():
    from squarepeg.defect_extraction.sparse_gate_extraction import sparse_defect_allocation

    areas = [0.01, 0.008, -0.002, 0.007, 0.006]
    alloc = sparse_defect_allocation(areas, epsilon=0.025, lambda_qr=0.005)
    assert alloc.join_negligible
    assert alloc.dominant_sign_mass >= 0.025 / 4


@pytest.mark.fast
def test_t060_sparse_certificate():
    g = example_four_gate_graph()
    cert = certify_t060(g, example_bump_polygon(), m=10, r=0.0002, epsilon=0.025)
    assert cert.sparse
    assert cert.status == "PROVED_LOCALLY_SPARSE"


@pytest.mark.fast
def test_dense_gate_classification():
    d = classify_gate_density(200, 0.001)
    assert d.regime == "DENSE"


@pytest.mark.fast
def test_normalized_gate_measure():
    gates = [NormalizedGate(f"g{i}", (math.cos(i), math.sin(i)), i) for i in range(8)]
    m = normalize_hull(gates, diameter_r=0.1)
    assert m.diameter == 1.0
    assert len(m.weights) == 8


@pytest.mark.fast
def test_gate_word_ordered_vs_scrambled():
    ordered = classify_gate_word(["g0", "g1", "g2", "g3"], ["g0", "g1", "g2", "g3"])
    scrambled = classify_gate_word(["g0", "g1", "g2", "g3"], ["g2", "g0", "g3", "g1"])
    assert ordered.order_class == "ASYMPTOTICALLY_ORDERED"
    assert scrambled.order_class == "PERSISTENTLY_SCRAMBLED"


@pytest.mark.fast
def test_gate_block_cross_terms():
    blocks = partition_gate_blocks([f"g{i}" for i in range(20)], m0=8, r=0.05)
    assert len(blocks.blocks) == 3
    assert blocks.cross_block_join_bound >= 0


@pytest.mark.fast
def test_winding_amplification():
    w = winding_amplification(0.025, 0.01)
    assert w > 100


@pytest.mark.fast
def test_concentrated_subblock():
    gates = [f"g{i}" for i in range(12)]
    sp = [0.05] * 12
    areas = [0.001] * 10 + [0.015, 0.012]
    conc = extract_concentrated_subblock(gates, sp, areas, r=0.08, epsilon=0.025)
    assert conc.subblock is not None or conc.descent_class == "TERMINATED"


@pytest.mark.fast
def test_diffuse_gate_example():
    gates = [NormalizedGate(f"g{i}", (i / 25, 0.0), i) for i in range(25)]
    m = normalize_hull(gates, diameter_r=0.05)
    diff = classify_diffuse_limit([m], 0.005)
    assert diff.formalism in ("NONCROSSING_LAMINATION", "SIGNED_MEASURE")
    assert diff.measure_limit.measure_type in ("DIFFUSE", "MULTICENTER", "FINITELY_SUPPORTED")


@pytest.mark.fast
def test_t061_dense_trichotomy():
    rec = DenseGateRecord(
        cluster_id="D1",
        gate_count=24,
        diameter_r=0.04,
        lambda_mr=0.96,
        hull_order=[f"g{i}" for i in range(24)],
        param_order=[f"g{i}" for i in range(24)],
        gate_positions=[(math.cos(2 * math.pi * i / 24), math.sin(2 * math.pi * i / 24)) for i in range(24)],
        attachment_area=0.025,
    )
    audit = audit_dense_gate_trichotomy(rec)
    assert audit.dense
    assert audit.status == "PROVED_LOCALLY_CLASSIFICATION"


@pytest.mark.fast
def test_t062_finite_center():
    positions = [(0, 0), (0.1, 0), (0.2, 0), (1, 1), (1.1, 1)]
    cert = certify_finite_center_dense(positions, [f"g{i}" for i in range(5)], k=3, r=0.08)
    assert cert.center_count >= 1
