"""Directive 036 — positive-inversion gate orders and monotone block decomposition."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.cyclic_gate_order import encode_cyclic_order
from squarepeg.defect_extraction.finite_gate_permutation import (
    gate_permutation,
    inv_density,
    inv_weighted,
    longest_decreasing_subsequence,
)
from squarepeg.defect_extraction.finite_width_gate_surgery import certify_t073
from squarepeg.defect_extraction.gate_inversion_energy import inversion_energy
from squarepeg.defect_extraction.gate_permuton import audit_gate_permuton, discrete_permuton
from squarepeg.defect_extraction.infinite_gate_measure import WeightedGate, gate_set_of_leaf
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_order_blocks import select_measurable_blocks
from squarepeg.defect_extraction.monotone_gate_width import audit_monotone_width, monotone_width
from squarepeg.defect_extraction.noncrossing_order_width import certify_t074
from squarepeg.defect_extraction.order_block_signature import audit_cross_block_signature
from squarepeg.defect_extraction.parameter_component_order import certify_t072r
from squarepeg.defect_extraction.positive_inversion_reduction import certify_t071r, certify_t065o
from squarepeg.defect_extraction.countable_order_blocks import certify_t073i
from squarepeg.defect_extraction.winding_function import winding_grid
from squarepeg.defect_extraction.winding_lamination import build_diffuse_lamination


def _leaf() -> EssentialLeaf:
    return EssentialLeaf("L1", 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.5, None, [])


def _inverted_finite_width_gate_set():
    """One inversion, finite monotone width."""
    leaf = _leaf()
    gs = gate_set_of_leaf(leaf, count=6, scale_base=0.08)
    gates = list(gs.gates)
    if len(gates) >= 2:
        gates[0], gates[1] = gates[1], gates[0]
        gates[0] = WeightedGate(
            gates[0].gate_id, gates[0].point, 0.15, gates[0].scale_weight, gates[0].boundary_index
        )
        gates[1] = WeightedGate(
            gates[1].gate_id, gates[1].point, 0.05, gates[1].scale_weight, gates[1].boundary_index
        )
    from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet

    return InfiniteGateSet(
        leaf_id=leaf.leaf_id,
        gate_class="FINITE",
        gates=gates,
        closed=True,
        total_mass=sum(g.scale_weight for g in gates),
    )


def _lamination():
    w = winding_grid([(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)], grid_n=14)
    return build_diffuse_lamination(w, [f"g{i}" for i in range(12)], area_total=0.025, eta=0.005)


@pytest.mark.fast
def test_cyclic_seam_invariance():
    gs = gate_set_of_leaf(_leaf(), count=6)
    order = encode_cyclic_order(gs)
    assert order.seam_invariant


@pytest.mark.fast
def test_weighted_inversion_energy():
    gs = _inverted_finite_width_gate_set()
    perm = gate_permutation(gs)
    inv = inversion_energy(gs)
    assert perm.converges_to_measure or perm.inv_density > 0
    assert inv.energy >= 0


@pytest.mark.fast
def test_monotone_width():
    gs = _inverted_finite_width_gate_set()
    perm = gate_permutation(gs)
    w = monotone_width(perm.pi)
    lds = longest_decreasing_subsequence(perm.pi)
    assert w == lds


@pytest.mark.fast
def test_decreasing_subsequences():
    gs = _inverted_finite_width_gate_set()
    perm = gate_permutation(gs)
    assert longest_decreasing_subsequence(perm.pi) >= 1


@pytest.mark.fast
def test_measurable_monotone_blocks():
    gs = _inverted_finite_width_gate_set()
    sel = select_measurable_blocks(gs, K=4)
    assert sel.measurable
    assert sel.block_count >= 1


@pytest.mark.fast
def test_finite_width_cross_block_signatures():
    gs = _inverted_finite_width_gate_set()
    sel = select_measurable_blocks(gs, K=4)
    cross = audit_cross_block_signature(sel, K=4)
    assert cross.cross_area >= 0


@pytest.mark.fast
def test_countable_block_tails():
    gs = gate_set_of_leaf(_leaf(), count=16)
    cert = certify_t073i(gs)
    assert cert.status in ("CONJECTURAL_EXTENSION", "PROVED_LOCALLY")


@pytest.mark.fast
def test_permuton_convergence():
    gs = _inverted_finite_width_gate_set()
    audit = audit_gate_permuton(gs)
    assert audit.weak_limit_exists


@pytest.mark.fast
def test_parameter_component_graph():
    cert = certify_t072r(_leaf(), [1, 2, 3, 10, 11], K=4)
    assert cert.graph.component_count >= 1


@pytest.mark.fast
def test_t073_certificate():
    gs = _inverted_finite_width_gate_set()
    cert = certify_t073(gs, _leaf(), K=4)
    assert cert.status == "PROVED_LOCALLY"
    assert cert.finite_width
    assert cert.cross_block_vanishing


@pytest.mark.fast
def test_t074_classification():
    gs = gate_set_of_leaf(_leaf(), count=14)
    cert = certify_t074(gs, K=4)
    assert cert.outcome in (
        "INFINITE_INTRUSION_RAY",
        "UNBOUNDED_BRANCHING",
        "NON_JORDAN_LIMIT",
        "PARAMETER_DISCONNECTED",
        "MULTICENTER_DECOMPOSITION",
        "FINITE_WIDTH_SURGERY",
    )


@pytest.mark.fast
def test_t071r_classification():
    gs = _inverted_finite_width_gate_set()
    cert = certify_t071r(gs, K=4)
    assert cert.outcome in (
        "FINITE_MONOTONE_WIDTH",
        "COUNTABLE_SUMMABLE_BLOCKS",
        "UNBOUNDED_WIDTH_T074",
        "DISCONNECTED_CONCENTRATION",
        "DIFFUSE_PERMUTON",
        "NON_JORDAN",
    )


@pytest.mark.fast
def test_t065o_reduction():
    lam = _lamination()
    cert = certify_t065o(lam, list(range(12)), K=4)
    assert cert.outcome in (
        "T066", "T068", "T069", "T068I", "T073", "T073I",
        "INTRUSION_TREE", "NON_JORDAN", "DISCONNECTED", "DIFFUSE_PERMUTON", "INFINITE_CENTER",
    )
