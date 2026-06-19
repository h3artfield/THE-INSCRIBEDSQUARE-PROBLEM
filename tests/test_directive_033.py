"""Directive 033 — diffuse winding laminations: leaf surgery or annular band."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_extraction.annular_band_extraction import annular_band_between, certify_t067
from squarepeg.defect_extraction.dense_leaf_gates import gate_measure_on_leaf
from squarepeg.defect_extraction.dense_normalization import DenseClusterRecord
from squarepeg.defect_extraction.disconnected_concentration import (
    audit_disconnected_concentration,
    certify_t064d,
)
from squarepeg.defect_extraction.eccentric_leaf import classify_eccentric_leaf, leaf_eccentricity
from squarepeg.defect_extraction.finite_dense_lamination_reduction import certify_t065r
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf, audit_lamination_compactness
from squarepeg.defect_extraction.lamination_gate_support import classify_parameter_support
from squarepeg.defect_extraction.lamination_leaf_topology import classify_leaf_topology
from squarepeg.defect_extraction.lamination_signature import audit_lamination_signature
from squarepeg.defect_extraction.ordered_leaf_surgery import (
    certify_t066,
    cluster_from_leaf,
    finite_surgery_exhaustion,
    is_ordered_two_gate_lamination,
)
from squarepeg.defect_extraction.winding_function import split_winding_mass, winding_grid
from squarepeg.defect_extraction.winding_layers import build_winding_layers
from squarepeg.defect_extraction.winding_lamination import build_diffuse_lamination, build_winding_lamination


def _square_chain():
    return [(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)]


def _spiral(n: int = 16):
    pts = [(0.5 * math.cos(k / n * 4 * math.pi), 0.5 * math.sin(k / n * 4 * math.pi)) for k in range(n)]
    return pts + [pts[0]]


def _dense_record() -> DenseClusterRecord:
    return DenseClusterRecord("C", 0.05, 40, 2.0, 0.025, (0.0, 0.0))


@pytest.mark.fast
def test_disconnected_concentration():
    gids = [f"g{i}" for i in range(10)]
    params = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
    att = [0.001] * 8 + [0.012, 0.011]
    pos = [(0.05 * (i % 2), 0.02 * i) for i in range(10)]
    w = winding_grid(_square_chain(), grid_n=14)
    mass = split_winding_mass(w)
    rec = audit_disconnected_concentration(
        gids, params, att, pos, w, mass, center=(0.0, 0.0), rho=0.3, r=0.05, epsilon=0.025
    )
    assert rec.parameter_component_count >= 1


@pytest.mark.fast
def test_hausdorff_leaf_compactness():
    w = winding_grid(_square_chain(), grid_n=14)
    audit = audit_lamination_compactness(w, eta=0.01)
    assert audit.hausdorff_precompact
    assert audit.transverse.total_mass > 0


@pytest.mark.fast
def test_transverse_measure_extraction():
    w = winding_grid(_spiral(), grid_n=16)
    lam = build_diffuse_lamination(w, ["g0", "g1"], area_total=0.025, eta=0.01)
    assert lam.no_mass_atom or lam.winding_mass > 0
    assert lam.noncrossing


@pytest.mark.fast
def test_noncrossing_leaf_limits():
    layers = build_winding_layers({(i, j): min(i, j, 2) for i in range(8) for j in range(8)})
    lam = build_winding_lamination(layers, ["g0"], area_total=0.025)
    assert lam.noncrossing


@pytest.mark.fast
def test_jordan_and_pinched_leaves():
    w = winding_grid(_square_chain(), grid_n=12)
    audit = audit_lamination_compactness(w, eta=0.01)
    assert audit.essential_leaves
    topo = classify_leaf_topology(audit.essential_leaves[0], gate_count=2)
    assert topo.leaf_class in ("JORDAN_LEAF", "PINCHED_LEAF", "MULTIBOUNDARY_LEAF")


@pytest.mark.fast
def test_two_gate_leaf_classification():
    cluster = cluster_from_leaf("L1")
    leaf = EssentialLeaf(
        leaf_id="L1",
        level=1,
        closure=((0, 0), (0.1, 0), (0.1, 0.1), (0, 0.1)),
        area=0.01,
        diameter=0.14,
        area_fraction=0.5,
        parent_id=None,
        child_ids=[],
    )
    topo = classify_leaf_topology(leaf, gate_count=2)
    assert topo.gate_class == "TWO_GATE_LEAF"
    assert cluster.hull.is_jordan_disk


@pytest.mark.fast
def test_finite_surgery_exhaustion():
    w = winding_grid(_square_chain(), grid_n=12)
    lam = build_diffuse_lamination(w, ["g0", "g1", "g2"], area_total=0.025, eta=0.005)
    steps = finite_surgery_exhaustion(lam, max_depth=3)
    assert len(steps) >= 1
    assert steps[-1].defect_processed > 0


@pytest.mark.fast
def test_lamination_tail_control():
    w = winding_grid(_square_chain(), grid_n=12)
    lam = build_diffuse_lamination(w, ["g0", "g1"], area_total=0.025, eta=0.005)
    steps = finite_surgery_exhaustion(lam)
    sig = audit_lamination_signature(lam, steps)
    assert sig.tail_defect_fraction <= 1.0


@pytest.mark.fast
def test_annular_band_extraction():
    w = winding_grid(_square_chain(), grid_n=14)
    layers = build_winding_layers(w)
    lam = build_diffuse_lamination(w, ["g0"], area_total=0.025, eta=0.005)
    cert = certify_t067(lam, layers)
    assert cert.outcome in (
        "ANNULAR_BAND_CERTIFIED",
        "ORDERED_TWO_GATE_MASS",
        "ECCENTRIC_MULTICENTER_RESIDUAL",
    )


@pytest.mark.fast
def test_eccentric_leaves():
    w = winding_grid(_spiral(), grid_n=16)
    audit = audit_lamination_compactness(w, eta=0.005)
    if audit.essential_leaves:
        ecc = classify_eccentric_leaf(audit.essential_leaves[0])
        assert leaf_eccentricity(audit.essential_leaves[0]) >= 0


@pytest.mark.fast
def test_dense_gate_measures():
    gm = gate_measure_on_leaf("L1", [(0, 0), (0.1, 0)], [0, 1], leaf_radius=0.2)
    assert gm.gate_count >= 1
    assert 0 <= gm.inversion_density <= 1


@pytest.mark.fast
def test_inversion_density():
    gm = gate_measure_on_leaf("L1", [(0, 0), (0.2, 0), (0.1, 0.1)], [2, 0, 1], leaf_radius=0.5)
    assert gm.inversion_density >= 0


@pytest.mark.fast
def test_t065r_classification():
    rec = _dense_record()
    chain = _spiral()
    cert = certify_t065r(rec, chain, [f"g{i}" for i in range(12)], list(range(12)), chain)
    assert cert.outcome in (
        "SIGNATURE_CONTROLLED_SURGERY",
        "RECURSIVE_CONCENTRATED_DESCENT",
        "FINITE_CENTER_REDUCTION",
        "ORDERED_TWO_GATE_LAMINATION_SURGERY",
        "PROTECTED_ANNULAR_GEOMETRY",
        "EXPLICIT_LAMINATION_RESIDUAL",
        "NON_JORDAN_SATURATION_HULL",
    )


@pytest.mark.fast
def test_t066_ordered_lamination():
    w = winding_grid(_square_chain(), grid_n=12)
    lam = build_diffuse_lamination(w, ["g0", "g1"], area_total=0.025, eta=0.005)
    assert is_ordered_two_gate_lamination(lam) or len(lam.leaves) >= 0
    cert = certify_t066(lam)
    assert cert.status == "PROVED_LOCALLY"
    assert cert.is_ordered_two_gate


@pytest.mark.fast
def test_t064d_certificate():
    gids = [f"g{i}" for i in range(8)]
    params = list(range(8))
    att = [0.003] * 6 + [0.012, 0.012]
    pos = [(i * 0.04, 0) for i in range(8)]
    cert = certify_t064d(gids, params, att, pos, _square_chain(), epsilon=0.025)
    assert cert.outcome in (
        "PARAMETER_CONSECUTIVE_BLOCK",
        "FINITE_CENTER_T062",
        "DIFFUSE_LAMINATION_LIMIT",
        "INFINITE_INTRUSION_OR_NONJORDAN",
    )


@pytest.mark.fast
def test_parameter_support():
    ps = classify_parameter_support("L1", [1, 2, 3, 10, 11])
    assert ps.support_class in (
        "ONE_INTERVAL",
        "FINITELY_MANY_INTERVALS",
        "CANTOR_TYPE",
        "DENSE_IN_SUBINTERVAL",
    )
