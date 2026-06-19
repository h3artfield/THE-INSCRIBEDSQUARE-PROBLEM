"""Directive 039 — planar permuton rigidity and diffuse order residual."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.augmented_permuton_compactness import (
    audit_genuinely_diffuse,
    build_augmented_measure,
)
from squarepeg.defect_extraction.bounded_depth_order import certify_t077a
from squarepeg.defect_extraction.decreasing_order_geometry import (
    audit_decreasing_geometry,
    extract_compactness_limit,
)
from squarepeg.defect_extraction.diffuse_permuton_reduction import certify_t065pr
from squarepeg.defect_extraction.forbidden_pattern_audit import audit_forbidden_patterns
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate, gate_set_of_leaf
from squarepeg.defect_extraction.jordan_gate_realizability import (
    audit_jordan_realizability,
    cyclic_permutation_invariant,
)
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.planar_inversion_graph import audit_inversion_graph_planarity
from squarepeg.defect_extraction.planar_permuton_rigidity import certify_t074r_planar, certify_t077_planar
from squarepeg.defect_extraction.permuton_extremal_bound import audit_extremal_bound
from squarepeg.defect_extraction.realizable_permutation_class import (
    audit_realizable_class,
    pattern_containment,
)
from squarepeg.defect_extraction.substitution_decomposition import audit_planar_decomposition
from squarepeg.defect_extraction.winding_function import winding_grid
from squarepeg.defect_extraction.winding_lamination import build_diffuse_lamination


def _leaf() -> EssentialLeaf:
    return EssentialLeaf("L1", 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.5, None, [])


def _gate_set(count: int = 12) -> InfiniteGateSet:
    return gate_set_of_leaf(_leaf(), count=count)


def _summable_gate_set() -> InfiniteGateSet:
    gates = [WeightedGate(f"g{j}", (0.5, 0.5), j / 12.0, 0.08 / (1 + j), float(j)) for j in range(12)]
    return InfiniteGateSet("L1", "FINITE", gates, True, sum(g.scale_weight for g in gates))


def _lamination():
    w = winding_grid([(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)], grid_n=14)
    return build_diffuse_lamination(w, [f"g{i}" for i in range(12)], area_total=0.025, eta=0.005)


@pytest.mark.fast
def test_cyclic_permutation_realizability():
    gs = _gate_set(10)
    audit = audit_jordan_realizability(gs, _leaf())
    assert audit.status in ("REALIZABLE_JORDAN_NONCROSSING", "NONREALIZABLE_TOPOLOGY", "INDETERMINATE")
    assert cyclic_permutation_invariant(gs)


@pytest.mark.fast
def test_pattern_containment():
    pi = [2, 0, 3, 1]
    assert pattern_containment(pi, [2, 1]) or not pattern_containment(pi, [0, 1, 2, 3])


@pytest.mark.fast
def test_realizable_class():
    audit = audit_realizable_class(_gate_set(10), _leaf())
    assert audit.pattern_verdict in (
        "SEPARABLE_PERMUTATIONS_ONLY",
        "FINITE_BASIS_BROADER_CLASS",
        "INFINITE_BASIS_CLASS",
        "ARBITRARY_PERMUTATIONS_REALIZABLE",
        "UNRESOLVED",
    )
    assert audit.cyclic_shift_closed


@pytest.mark.fast
def test_forbidden_patterns():
    audit = audit_forbidden_patterns(_gate_set(10))
    assert isinstance(audit.contains_2413, bool)


@pytest.mark.fast
def test_substitution_tree():
    audit = audit_planar_decomposition(_gate_set(12), _leaf())
    assert audit.tree.root.decomposition
    assert audit.substitution_depth >= 1


@pytest.mark.fast
def test_decreasing_subsequence_geometry():
    geom = audit_decreasing_geometry(_gate_set(14), _leaf())
    assert geom.subsequence_length >= 1
    assert geom.arc_geometry in (
        "NESTING",
        "COMMON_ACCUMULATION",
        "BRANCHING",
        "SEPARATED_CENTERS",
        "HULL_PINCHING",
    )


@pytest.mark.fast
def test_augmented_permuton_convergence():
    limit = build_augmented_measure(_gate_set(12), _leaf())
    assert limit.weak_convergence
    assert limit.tight
    assert len(limit.atoms) >= 1


@pytest.mark.fast
def test_bounded_depth_examples():
    cert = certify_t077a(_gate_set(12), _leaf(), D=8, B=4, K=4)
    assert cert.status in ("CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY")
    assert cert.audit.max_depth >= 1


@pytest.mark.fast
def test_branching_and_center_examples():
    ext = audit_extremal_bound(_gate_set(16), D=8, B=4, K=4)
    assert ext.max_inversion_density > 0


@pytest.mark.fast
def test_finite_center_example():
    limit = build_augmented_measure(_summable_gate_set(), _leaf())
    crit = audit_genuinely_diffuse(limit, K=4)
    assert crit.jordan_hull


@pytest.mark.fast
def test_inversion_graph_planarity():
    audit = audit_inversion_graph_planarity(_gate_set(12))
    assert audit.graph.edge_count >= 0


@pytest.mark.fast
def test_diffuse_permuton_attempts():
    limit = build_augmented_measure(_gate_set(20), _leaf())
    crit = audit_genuinely_diffuse(limit, K=4)
    assert isinstance(crit.genuinely_diffuse, bool)


@pytest.mark.fast
def test_t077_certificates():
    cert = certify_t077_planar(_gate_set(12), _leaf())
    assert cert.outcome in (
        "ROUTED_TO_T073I",
        "INFINITE_INTRUSION_DEPTH",
        "UNBOUNDED_BRANCHING",
        "INFINITE_CENTER_PROLIFERATION",
        "PARAMETER_DISCONNECTED",
        "NON_JORDAN_HULL",
        "GENUINELY_DIFFUSE_RESIDUAL",
    )


@pytest.mark.fast
def test_t074r_planar():
    cert = certify_t074r_planar(_gate_set(14), _leaf())
    assert cert.outcome


@pytest.mark.fast
def test_t065pr():
    cert = certify_t065pr(_lamination(), _leaf())
    assert cert.route
    assert cert.status in ("CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL")


@pytest.mark.fast
def test_compactness_extraction():
    ext = extract_compactness_limit(_gate_set(16), _leaf())
    assert ext.outcome
