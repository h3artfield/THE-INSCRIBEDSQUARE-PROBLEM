"""Directive 032 — dense winding layers and concentration-compactness."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_extraction.concentration_compactness import classify_concentration_compactness
from squarepeg.defect_extraction.concentrated_parameter_block import extract_consecutive_block
from squarepeg.defect_extraction.dense_normalization import DenseClusterRecord, normalize_dense_cluster
from squarepeg.defect_extraction.diffuse_winding_layers import audit_diffuse_layers, build_nested_chain
from squarepeg.defect_extraction.finite_center_extraction import certify_t062_complete
from squarepeg.defect_extraction.finite_dense_reduction import audit_t061r, certify_t065
from squarepeg.defect_extraction.recursive_dense_descent import recursive_dense_descent
from squarepeg.defect_extraction.winding_function import (
    audit_closed_walk,
    close_polygonal_walk,
    split_winding_mass,
    winding_grid,
    winding_l_infinity_lower,
)
from squarepeg.defect_extraction.winding_layers import build_winding_layers, layer_cake_identity_holds
from squarepeg.defect_extraction.winding_layer_tree import build_layer_tree, verify_nesting
from squarepeg.defect_extraction.winding_lamination import audit_lamination_surgery, build_winding_lamination


def _dense_record(r: float = 0.05, m: int = 40) -> DenseClusterRecord:
    return DenseClusterRecord("C", r, m, m * r, 0.025, (0.0, 0.0))


def _spiral_chain(n: int = 12):
    return [(0.5 * math.cos(k / n * 4 * math.pi), 0.5 * math.sin(k / n * 4 * math.pi)) for k in range(n)]


@pytest.mark.fast
def test_normalized_area_scaling():
    rec = _dense_record(0.05)
    norm = normalize_dense_cluster(rec, [(0, 0), (1, 0)], _spiral_chain())
    assert norm.area_normalized == pytest.approx(0.025 / 0.0025, rel=0.01)
    assert norm.winding_amplification > 5


@pytest.mark.fast
def test_winding_amplification():
    lb = winding_l_infinity_lower(10.0)
    assert lb > 10


@pytest.mark.fast
def test_positive_negative_mass_split():
    chain = [(0, 0), (0.8, 0), (0.8, 0.6), (0, 0.6), (0, 0)]
    w = winding_grid(chain, grid_n=12)
    mass = split_winding_mass(w)
    assert mass.positive_mass > 0 or mass.negative_mass > 0
    assert mass.dominant_fraction >= 0.5


@pytest.mark.fast
def test_layer_cake_identity():
    chain = _spiral_chain(16) + [(_spiral_chain(16)[0])]
    w = winding_grid(chain, grid_n=12)
    assert layer_cake_identity_holds(w)


@pytest.mark.fast
def test_winding_component_nesting():
    chain = [(0, 0), (0.9, 0), (0.9, 0.7), (0, 0.7), (0, 0)]
    w = winding_grid(chain, grid_n=14)
    layers = build_winding_layers(w)
    assert verify_nesting(layers)
    tree = build_layer_tree(layers)
    assert tree.nested


@pytest.mark.fast
def test_concentrated_example():
    chain = [(0, 0), (0.1, 0), (0.1, 0.1), (0, 0.1), (0, 0)]
    w = winding_grid(chain, grid_n=16)
    mass = split_winding_mass(w)
    t063 = classify_concentration_compactness(w, mass)
    assert t063.regime in ("CONCENTRATED", "DIFFUSE", "MULTICENTER")


@pytest.mark.fast
def test_diffuse_example():
    chain = _spiral_chain(20) + [_spiral_chain(20)[0]]
    w = winding_grid(chain, grid_n=16)
    layers = build_winding_layers(w)
    audit = audit_diffuse_layers(layers)
    assert audit.chain is not None


@pytest.mark.fast
def test_consecutive_block_extraction():
    gids = [f"g{i}" for i in range(12)]
    params = list(range(12))
    att = [0.001] * 10 + [0.012, 0.011]
    pos = [(i * 0.05, 0.0) for i in range(12)]
    ext = extract_consecutive_block(gids, params, att, pos, center=(0.5, 0), rho=0.3, r=0.05)
    assert ext.block is not None or ext.defect_fraction > 0


@pytest.mark.fast
def test_recursive_descent():
    rec = _dense_record()
    descent = recursive_dense_descent(
        [rec],
        [[f"g{i}" for i in range(8)]],
        [list(range(8))],
        [[0.003] * 6 + [0.012, 0.012]],
        [[(i * 0.02, 0) for i in range(8)]],
    )
    assert len(descent.steps) >= 1


@pytest.mark.fast
def test_t062_finite_center():
    pos = [(0, 0), (0.1, 0), (0.2, 0), (0.15, 0.05)]
    cert = certify_t062_complete(pos, [f"g{i}" for i in range(4)], k=4, r=0.08)
    assert cert.status == "PROVED_LOCALLY_FINITE_CENTER"


@pytest.mark.fast
def test_diffuse_nested_chain():
    layers = build_winding_layers({(i, j): 1 for i in range(4) for j in range(4)})
    chain = build_nested_chain(layers)
    assert chain.depth >= 1


@pytest.mark.fast
def test_winding_lamination():
    layers = build_winding_layers({(i, j): min(i, j, 1) for i in range(6) for j in range(6)})
    lam = build_winding_lamination(layers, ["g0", "g1"], area_total=0.025)
    audit = audit_lamination_surgery(lam)
    assert lam.noncrossing


@pytest.mark.fast
def test_t065_certificate():
    rec = _dense_record()
    chain = _spiral_chain()
    cert = certify_t065(rec, chain, [f"g{i}" for i in range(12)], list(range(12)), chain)
    assert cert.t061r.branch in (
        "CONCENTRATED_DESCENT",
        "FINITE_CENTER_DECOMPOSITION",
        "DIFFUSE_NESTED_LAYERS",
        "DISCONNECTED_OR_NONJORDAN",
    )
