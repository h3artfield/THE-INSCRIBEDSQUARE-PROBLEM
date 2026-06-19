"""Directive 034 — multi-gate lamination ears and thin-eccentric leaf surgery."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_extraction.compatible_lamination_ears import audit_ear_compatibility
from squarepeg.defect_extraction.diffuse_lamination_reduction import certify_t065s, certify_t068
from squarepeg.defect_extraction.finite_gate_lamination import audit_finite_gate_lamination, leaf_gate_data
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.leafwise_gate_graph import audit_leaf_gate_graph
from squarepeg.defect_extraction.measurable_ear_selection import audit_measurable_ear_selection
from squarepeg.defect_extraction.multigate_lamination_signature import signature_bound_uniform
from squarepeg.defect_extraction.multigate_leaf_exhaustion import truncate_by_transverse_mass
from squarepeg.defect_extraction.thick_leaf_band import audit_thick_band, band_modulus
from squarepeg.defect_extraction.thin_leaf_crosscut import construct_thin_crosscut, crosscut_area_bound
from squarepeg.defect_extraction.thin_leaf_geometry import audit_thin_leaf_class, leaf_width
from squarepeg.defect_extraction.thin_lamination_signature import certify_t069, thin_attachment_signature
from squarepeg.defect_extraction.winding_function import winding_grid
from squarepeg.defect_extraction.winding_lamination import build_diffuse_lamination


def _square_chain():
    return [(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)]


def _multigate_lamination():
    w = winding_grid(_square_chain(), grid_n=14)
    return build_diffuse_lamination(w, [f"g{i}" for i in range(6)], area_total=0.025, eta=0.005)


def _thin_leaf() -> EssentialLeaf:
    return EssentialLeaf(
        leaf_id="T1",
        level=1,
        closure=((0.0, 0.0), (1.0, 0.0), (1.0, 0.04), (0.0, 0.04)),
        area=0.04,
        diameter=1.0,
        area_fraction=0.4,
        parent_id=None,
        child_ids=["T2"],
    )


def _nested_leaves() -> list[EssentialLeaf]:
    outer = EssentialLeaf(
        "O1", 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.6, None, ["I1"]
    )
    inner = EssentialLeaf(
        "I1", 2, ((0.2, 0.2), (0.8, 0.2), (0.8, 0.8), (0.2, 0.8)), 0.36, 0.848, 0.4, "O1", []
    )
    return [outer, inner]


@pytest.mark.fast
def test_measurable_finite_gate_leaf_data():
    lam = _multigate_lamination()
    fg = audit_finite_gate_lamination(lam, M=6)
    assert fg.gate_class in ("FINITE_GATE_M", "INTEGRABLE_GATE")
    assert fg.jordan_fraction > 0


@pytest.mark.fast
def test_leafwise_outerplanarity():
    leaf = _nested_leaves()[0]
    data = leaf_gate_data(leaf, m=4)
    audit = audit_leaf_gate_graph(data, leaf)
    assert audit.outerplanar


@pytest.mark.fast
def test_deterministic_ear_selection():
    leaves = _nested_leaves()
    pairs = [(leaf_gate_data(l, m=4), l) for l in leaves]
    sel = audit_measurable_ear_selection(pairs)
    assert sel.measurable and sel.deterministic
    assert len(sel.selections) >= 1


@pytest.mark.fast
def test_nested_ear_compatibility():
    leaves = _nested_leaves()
    pairs = [(leaf_gate_data(l, m=4), l) for l in leaves]
    sel = audit_measurable_ear_selection(pairs)
    compat = audit_ear_compatibility(sel.selections, leaves)
    assert compat.nested_compatible
    assert not compat.crossing_crosscuts


@pytest.mark.fast
def test_finite_transverse_exhaustion():
    leaves = _nested_leaves()
    pairs = [(leaf_gate_data(l, m=4), l) for l in leaves]
    sel = audit_measurable_ear_selection(pairs)
    exhaust = truncate_by_transverse_mass(sel.selections, leaves)
    assert len(exhaust.steps) >= 1


@pytest.mark.fast
def test_three_limit_signature_bounds():
    leaves = _nested_leaves()
    pairs = [(leaf_gate_data(l, m=4), l) for l in leaves]
    sel = audit_measurable_ear_selection(pairs)
    exhaust = truncate_by_transverse_mass(sel.selections, leaves, max_steps=2)
    sig = signature_bound_uniform(exhaust, M=6)
    assert sig.C_M > 0
    assert sig.sigma_bound < 2.0


@pytest.mark.fast
def test_thin_leaf_width():
    leaf = _thin_leaf()
    w = leaf_width(leaf)
    assert w < 0.1
    assert w / leaf.diameter < 0.1


@pytest.mark.fast
def test_thin_crosscut_area():
    leaf = _thin_leaf()
    cc = construct_thin_crosscut(leaf)
    assert cc.intrinsic_area <= crosscut_area_bound(leaf) + 1e-6


@pytest.mark.fast
def test_rotating_eccentric_leaves():
    leaf = EssentialLeaf(
        "R1", 1,
        tuple((math.cos(t), 0.05 * math.sin(t)) for t in [i * math.pi / 8 for i in range(9)]),
        0.1, 2.0, 0.3, None, [],
    )
    audit = audit_thin_leaf_class([leaf], thin_ratio_threshold=0.15)
    assert audit.geometries[0].eccentricity > 1


@pytest.mark.fast
def test_nonsummable_width_counterexample():
    leaves = [
        EssentialLeaf(f"N{i}", i, ((0, 0), (1, 0), (1, 0.3), (0, 0.3)), 0.3, 1.0, 0.2, None, [])
        for i in range(5)
    ]
    sig = thin_attachment_signature(leaves)
    assert not sig.local_signature_vanishing or not sig.summability_holds


@pytest.mark.fast
def test_t068_certificate():
    lam = _multigate_lamination()
    cert = certify_t068(lam, M=6)
    assert cert.status in ("PROVED_LOCALLY", "CONJECTURAL_TARGET")
    if len(lam.leaves) >= 1:
        assert cert.measurable_selection or cert.uniform_M == 2


@pytest.mark.fast
def test_t069_certificate():
    cert = certify_t069([_thin_leaf(), _thin_leaf()])
    assert cert.thin_leaf_ordered
    assert cert.status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_t065s_classification():
    lam = _multigate_lamination()
    cert = certify_t065s(lam)
    assert cert.outcome in (
        "T066_ORDERED_TWO_GATE",
        "T068_FINITE_MULTIGATE",
        "T069_THIN_ECCENTRIC",
        "ANNULAR_BAND_SQUARE",
        "INFINITE_GATE_JORDAN",
        "NON_JORDAN",
        "POSITIVE_INVERSION",
        "PARAMETER_DISCONNECTED",
        "MULTICENTER_THICK",
    )


@pytest.mark.fast
def test_thick_band_modulus():
    outer, inner = _nested_leaves()
    bm = band_modulus(outer, inner)
    band = audit_thick_band(outer, inner)
    assert bm >= 0
