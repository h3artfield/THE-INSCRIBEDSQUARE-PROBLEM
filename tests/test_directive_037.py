"""Directive 037 — countable monotone blocks and cross-block signature tails."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.block_tail_norm import audit_l1_block_signature, tail_variation
from squarepeg.defect_extraction.countable_block_increments import cross_block_area, finite_head_identity
from squarepeg.defect_extraction.countable_cross_signature import infinite_tail_stage, tail_interaction_bound
from squarepeg.defect_extraction.countable_order_reduction import certify_t065c, certify_t072s
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate, gate_set_of_leaf
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_countable_blocks import certify_t075, extend_decomposition_to_countable
from squarepeg.defect_extraction.measurable_order_blocks import MonotoneBlock
from squarepeg.defect_extraction.nonsummable_block_residual import audit_nonsummable_tail
from squarepeg.defect_extraction.summable_block_geometry import audit_summable_block_geometry
from squarepeg.defect_extraction.t073i_clean_room import audit_t073i_clean_room
from squarepeg.defect_extraction.t073i_surgery import certify_t073i_v2
from squarepeg.defect_extraction.unbounded_width_geometry import certify_t074r
from squarepeg.defect_extraction.winding_function import winding_grid
from squarepeg.defect_extraction.winding_lamination import build_diffuse_lamination


def _leaf() -> EssentialLeaf:
    return EssentialLeaf("L1", 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.5, None, [])


def _summable_countable_gate_set() -> InfiniteGateSet:
    """Harmonic-scale monotone stripes."""
    leaf = _leaf()
    gates: list[WeightedGate] = []
    for j in range(12):
        s = 0.08 / (1 + j)
        gates.append(
            WeightedGate(
                f"g{j}",
                (0.5 + 0.01 * j, 0.5),
                j / 12.0,
                s,
                float(j),
            )
        )
    return InfiniteGateSet("L1", "COUNTABLY_INFINITE", gates, True, sum(g.scale_weight for g in gates))


def _lamination():
    w = winding_grid([(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)], grid_n=14)
    return build_diffuse_lamination(w, [f"g{i}" for i in range(12)], area_total=0.025, eta=0.005)


@pytest.mark.fast
def test_finite_head_identity():
    decomp = extend_decomposition_to_countable(_summable_countable_gate_set(), target_blocks=6)
    ident = finite_head_identity(decomp.blocks[:4])
    assert ident.identity_holds


@pytest.mark.fast
def test_cross_block_wedge_estimate():
    from squarepeg.defect_extraction.countable_block_increments import block_variation

    a = block_variation(MonotoneBlock("A", ["g0"], 0.1, True, True))
    b = block_variation(MonotoneBlock("B", ["g1"], 0.1, True, True))
    pair = cross_block_area(a, b)
    assert pair.A_ij <= pair.bound + 1e-9


@pytest.mark.fast
def test_l1_block_signature():
    decomp = extend_decomposition_to_countable(_summable_countable_gate_set(), target_blocks=10)
    l1 = audit_l1_block_signature(decomp.blocks)
    assert l1.uniform_S


@pytest.mark.fast
def test_tail_interaction_bound():
    est = tail_interaction_bound(S=1.0, tau=0.05)
    assert est.cross_tail_bound == pytest.approx(0.5 * (0.1 + 0.0025), rel=0.01)
    assert est.vanishes_with_l1


@pytest.mark.fast
def test_summable_block_geometry_implies_l1():
    gs = _summable_countable_gate_set()
    decomp = extend_decomposition_to_countable(gs, target_blocks=10)
    geom = audit_summable_block_geometry(decomp.blocks, gs)
    assert geom.summable
    assert geom.implies_l1


@pytest.mark.fast
def test_measurable_countable_blocks_t075():
    cert = certify_t075(_summable_countable_gate_set())
    assert cert.status == "PROVED_LOCALLY"
    assert cert.decomposition.measurable


@pytest.mark.fast
def test_t073i_certificate():
    gs = _summable_countable_gate_set()
    cert = certify_t073i_v2(gs, _leaf())
    assert cert.status == "PROVED_LOCALLY"
    assert cert.l1_signature


@pytest.mark.fast
def test_t073i_clean_room():
    audit = audit_t073i_clean_room(_summable_countable_gate_set(), _leaf())
    assert audit.verdict == "T073I_CLEAN_ROOM_VERIFIED"
    assert audit.t045r_conjectural


@pytest.mark.fast
def test_infinite_tail_stage():
    decomp = extend_decomposition_to_countable(_summable_countable_gate_set(), target_blocks=10)
    stage = infinite_tail_stage(decomp.blocks, 4)
    assert stage.alpha_total < 0.5


@pytest.mark.fast
def test_nonsummable_counterexample():
    gs = gate_set_of_leaf(_leaf(), count=20)
    audit = audit_nonsummable_tail(gs)
    assert audit.outcome in (
        "T064D_CONCENTRATION",
        "T062_FINITE_CENTER",
        "INFINITE_INTRUSION_TREE",
        "DIFFUSE_PERMUTON",
        "INFINITE_CENTER",
        "NONSUMMABLE_RESIDUAL",
    )


@pytest.mark.fast
def test_t074r_classifier():
    cert = certify_t074r(gate_set_of_leaf(_leaf(), count=14))
    assert cert.status == "PROVED_LOCALLY_CLASSIFIER"


@pytest.mark.fast
def test_t072s():
    gs = _summable_countable_gate_set()
    cert = certify_t072s(_leaf(), gs, list(range(12)))
    assert cert.status in ("PROVED_LOCALLY", "CONJECTURAL_TARGET")


@pytest.mark.fast
def test_t065c():
    cert = certify_t065c(_lamination(), list(range(12)))
    assert cert.outcome in (
        "T066", "T068", "T069", "T068I", "T073", "T073I",
        "INTRUSION_TREE", "NON_JORDAN", "DISCONNECTED", "DIFFUSE_PERMUTON",
        "INFINITE_CENTER", "NONSUMMABLE_BLOCK", "UNBOUNDED_WIDTH",
    )
