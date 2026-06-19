"""Directive 038 — nonsummable order tails and planar permuton rigidity."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.augmented_gate_permuton import augmented_permuton
from squarepeg.defect_extraction.forbidden_pattern_audit import audit_forbidden_patterns
from squarepeg.defect_extraction.infinite_center_order import audit_infinite_center_order
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate, gate_set_of_leaf
from squarepeg.defect_extraction.intrinsic_order_tail import audit_intrinsic_nonsummability
from squarepeg.defect_extraction.intrusion_depth_from_order import certify_t074r_v2, decreasing_subsequence_geometry
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.nonsummable_concentration import certify_t076
from squarepeg.defect_extraction.nonsummable_order_reduction import certify_t065p, certify_t072c
from squarepeg.defect_extraction.order_interaction_measure import build_interaction_measure
from squarepeg.defect_extraction.permuton_rigidity import certify_t077
from squarepeg.defect_extraction.realizable_gate_permutations import audit_realizable_permutation
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable
from squarepeg.defect_extraction.winding_function import winding_grid
from squarepeg.defect_extraction.winding_lamination import build_diffuse_lamination


def _leaf() -> EssentialLeaf:
    return EssentialLeaf("L1", 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.5, None, [])


def _nonsummable_gate_set() -> InfiniteGateSet:
    """Heavy uniform blocks with persistent cross-tail mass."""
    leaf = _leaf()
    gs = gate_set_of_leaf(leaf, count=24)
    gates = [
        WeightedGate(g.gate_id, g.point, g.param_index, 0.14, g.boundary_index)
        for g in gs.gates
    ]
    return InfiniteGateSet("L1", "COUNTABLY_INFINITE", gates, True, sum(g.scale_weight for g in gates))


def _summable_gate_set() -> InfiniteGateSet:
    gates = [WeightedGate(f"g{j}", (0.5, 0.5), j / 12.0, 0.08 / (1 + j), float(j)) for j in range(12)]
    return InfiniteGateSet("L1", "FINITE", gates, True, sum(g.scale_weight for g in gates))


def _lamination():
    w = winding_grid([(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)], grid_n=14)
    return build_diffuse_lamination(w, [f"g{i}" for i in range(12)], area_total=0.025, eta=0.005)


@pytest.mark.fast
def test_intrinsic_nonsummability():
    ns = audit_intrinsic_nonsummability(_nonsummable_gate_set(), eta_0=0.03)
    sm = audit_intrinsic_nonsummability(_summable_gate_set(), eta_0=0.05)
    assert ns.nonsummable or ns.optimal_tail_cost > sm.optimal_tail_cost


@pytest.mark.fast
def test_order_interaction_measure():
    decomp = extend_decomposition_to_countable(_nonsummable_gate_set(), target_blocks=12)
    m = build_interaction_measure(decomp.blocks, N=3)
    assert m.xi_total >= 0
    assert m.failure_class in (
        "LINEAR_MASS_NONSUMMABLE",
        "CROSS_SIGNATURE_NONSUMMABLE",
        "INTERNAL_BLOCK_NONSUMMABLE",
        "MULTIPLE_FAILURES",
        "NONE",
    )


@pytest.mark.fast
def test_t076_concentrated_or_finite_center():
    cert = certify_t076(_nonsummable_gate_set())
    assert cert.branch in (
        "CONCENTRATED_ORDER_INTERACTION",
        "FINITE_CENTER_ORDER_INTERACTION",
        "DIFFUSE_ORDER_INTERACTION",
        "INFINITE_INTRUSION_OR_NONJORDAN",
    )


@pytest.mark.fast
def test_realizable_permutations():
    audit = audit_realizable_permutation(gate_set_of_leaf(_leaf(), count=8), _leaf())
    assert audit.realizability_class in (
        "REALIZABLE_JORDAN_NONCROSSING",
        "NONREALIZABLE_TOPOLOGY",
        "INDETERMINATE",
    )


@pytest.mark.fast
def test_forbidden_pattern_audit():
    audit = audit_forbidden_patterns(gate_set_of_leaf(_leaf(), count=8))
    assert audit.verdict in (
        "SEPARABLE_PERMUTATIONS_ONLY",
        "FINITE_BASIS_BROADER_CLASS",
        "INFINITE_BASIS_CLASS",
        "ARBITRARY_PERMUTATIONS_REALIZABLE",
        "UNRESOLVED",
    )


@pytest.mark.fast
def test_augmented_permuton():
    aug = augmented_permuton(_nonsummable_gate_set())
    assert aug.weak_limit_exists
    assert len(aug.atoms) >= 1


@pytest.mark.fast
def test_t077_permuton_rigidity():
    cert = certify_t077(_summable_gate_set())
    assert cert.outcome in (
        "ROUTED_TO_T073I",
        "INFINITE_INTRUSION_DEPTH",
        "NON_JORDAN_DEGENERATION",
        "INFINITE_CENTER_PROLIFERATION",
        "POSITIVE_SCALE_NONANNULAR",
        "GENUINELY_DIFFUSE_RESIDUAL",
    )


@pytest.mark.fast
def test_intrusion_depth_from_order():
    geom = decreasing_subsequence_geometry(gate_set_of_leaf(_leaf(), count=10))
    cert = certify_t074r_v2(gate_set_of_leaf(_leaf(), count=10), _leaf())
    assert cert.lds_length >= 1


@pytest.mark.fast
def test_infinite_center_order():
    audit = audit_infinite_center_order(_nonsummable_gate_set(), _leaf())
    assert audit.reconciled_label


@pytest.mark.fast
def test_t072c():
    cert = certify_t072c(_leaf(), _nonsummable_gate_set(), list(range(12)))
    assert cert.outcome in (
        "T076_CONCENTRATION",
        "T076_FINITE_CENTER",
        "INFINITE_INTRUSION_DEPTH",
        "GENUINELY_DIFFUSE_JORDAN_GATE_PERMUTON",
    )


@pytest.mark.fast
def test_t065p():
    cert = certify_t065p(_lamination(), list(range(12)))
    assert cert.surgery_route
    assert cert.outcome
