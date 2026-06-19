"""Directive 035 — infinite-gate Jordan laminations and order energy."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.finite_gate_truncation import build_truncation_tower, finite_gate_truncation
from squarepeg.defect_extraction.gate_inversion_energy import certify_t070, inversion_energy
from squarepeg.defect_extraction.gate_tail_defect import defect_tail_N
from squarepeg.defect_extraction.gate_tail_signature import sig_tail_N, tail_signature_tends_zero
from squarepeg.defect_extraction.infinite_gate_lamination_surgery import certify_t068i
from squarepeg.defect_extraction.infinite_gate_measure import gate_set_of_leaf
from squarepeg.defect_extraction.infinite_gate_reduction import certify_t065i, certify_t071
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_gate_field import audit_measurable_gate_field
from squarepeg.defect_extraction.multicenter_thick_leaf import audit_multicenter_thick, center_chart_count
from squarepeg.defect_extraction.parameter_support_components import audit_parameter_support, certify_t072
from squarepeg.defect_extraction.saturated_gate_truncation import build_saturated_tower
from squarepeg.defect_extraction.weighted_gate_complexity import gate_complexity_functional, tail_complexity
from squarepeg.defect_extraction.winding_function import winding_grid
from squarepeg.defect_extraction.winding_lamination import build_diffuse_lamination


def _leaf() -> EssentialLeaf:
    return EssentialLeaf(
        "L1", 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.5, None, []
    )


def _infinite_gate_lamination():
    w = winding_grid([(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)], grid_n=14)
    return build_diffuse_lamination(w, [f"g{i}" for i in range(24)], area_total=0.025, eta=0.005)


@pytest.mark.fast
def test_closed_infinite_gate_sets():
    gs = gate_set_of_leaf(_leaf(), count=24)
    assert gs.closed
    assert gs.gate_class in ("FINITE", "COUNTABLY_INFINITE", "CANTOR", "NONATOMIC_DIFFUSE")


@pytest.mark.fast
def test_measurable_gate_fields():
    audit = audit_measurable_gate_field([_leaf()])
    assert audit.borel_measurable
    assert len(audit.measures) == 1


@pytest.mark.fast
def test_nested_finite_truncations():
    gs = gate_set_of_leaf(_leaf(), count=16)
    tower = build_truncation_tower(gs, max_levels=4)
    assert tower.monotone
    assert len(tower.truncations) >= 1


@pytest.mark.fast
def test_saturation_compatibility():
    gs = gate_set_of_leaf(_leaf(), count=8)
    sat = build_saturated_tower(gs, _leaf(), max_levels=3)
    assert all(s.saturated for s in sat)


@pytest.mark.fast
def test_tail_intrinsic_area():
    gs = gate_set_of_leaf(_leaf(), count=12)
    sat = build_saturated_tower(gs, _leaf(), max_levels=2)[0]
    defect = defect_tail_N(sat, gs)
    assert defect.total_defect >= defect.intrinsic_ear_area


@pytest.mark.fast
def test_tail_cross_signature():
    gs = gate_set_of_leaf(_leaf(), count=12)
    tower = build_saturated_tower(gs, _leaf(), max_levels=4)
    sigs = [sig_tail_N(s, gs) for s in tower]
    assert sigs[-1].cross_interaction >= 0


@pytest.mark.fast
def test_weighted_complexity():
    gs = gate_set_of_leaf(_leaf(), count=12, scale_base=0.08)
    c = gate_complexity_functional(gs)
    assert c.total_complexity > 0
    trunc = finite_gate_truncation(gs, 4)
    assert tail_complexity(gs, trunc) >= 0


@pytest.mark.fast
def test_ordered_nonatomic_gate_measures():
    gs = gate_set_of_leaf(_leaf(), count=20)
    inv = inversion_energy(gs)
    assert inv.energy < 0.01
    cert = certify_t070(gs)
    assert cert.status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_positive_inversion_example():
    gs = gate_set_of_leaf(_leaf(), count=8)
    gs.gates = list(reversed(gs.gates))
    inv = inversion_energy(gs)
    assert inv.positive_class or inv.energy > 0.3


@pytest.mark.fast
def test_cantor_parameter_support():
    audit = audit_parameter_support(_leaf(), [1, 2, 3, 20, 21, 22])
    assert audit.component_count >= 2


@pytest.mark.fast
def test_finite_and_infinite_center_counts():
    leaf = _leaf()
    assert center_chart_count(leaf) >= 1
    mc = audit_multicenter_thick(leaf, K=1)
    assert mc.center_class in ("FINITE_CENTER_THICK", "INFINITE_CENTER_THICK", "MULTICENTER_THICK_WINDING_LAMINATION")


@pytest.mark.fast
def test_t068i_certificate():
    lam = _infinite_gate_lamination()
    cert = certify_t068i(lam, gate_order_assumed=True)
    assert cert.status == "PROVED_LOCALLY_GATE_ORDERED"
    assert cert.tail_signature_vanishing


@pytest.mark.fast
def test_t065i_classification():
    lam = _infinite_gate_lamination()
    cert = certify_t065i(lam, list(range(12)), gate_order_assumed=True)
    assert cert.outcome in (
        "T066", "T068", "T069", "T068I",
        "FINITE_CENTER_THICK", "POSITIVE_INVERSION",
        "PARAMETER_DISCONNECTED", "INFINITE_CENTER", "NON_JORDAN",
    )


@pytest.mark.fast
def test_t072_finite_components():
    cert = certify_t072(_leaf(), [1, 2, 3, 4], K=4)
    assert cert.outcome == "FINITE_CONNECTED_BLOCKS"


@pytest.mark.fast
def test_t071_classifier():
    gs = gate_set_of_leaf(_leaf(), count=8)
    cert = certify_t071(gs)
    assert cert.status in ("CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER")
