"""Directive 021 annular-graph geometry tests."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_geometry.annular_graph import (
    AnnularGraphConstants,
    AnnularGraphPacket,
    RadialLayer,
    radial_gap_ratio,
    radial_layer_from_ellipse,
    validate_annular_graph,
)
from squarepeg.defect_geometry.annular_graph_certificate import (
    CERTIFIED_REGIME,
    C_ANN,
    certify_t036_n1_ann,
    example_certified_packet,
    export_reference_certificate_json,
)
from squarepeg.defect_geometry.eccentricity_audit import (
    audit_thin_ellipse,
    directive_020_falsification_excluded,
    no_successful_counterexample,
    search_annular_counterexamples,
)
from squarepeg.defect_geometry.packet_reference_bound import psi_from_constants, psi_annular_bound
from squarepeg.defect_geometry.positive_scale_compactness import annular_side_bound, positive_scale_corollary
from squarepeg.defect_geometry.radial_correspondence import (
    build_radial_correspondence,
    normalize_layer_pair,
    psi_from_correspondence,
)
from squarepeg.defect_geometry.recursive_annular_model import build_concentric_generations
from squarepeg.defect_geometry.reference_cyclic_certificate import certify_reference_annular, rho_cyc_reference


@pytest.mark.fast
def test_radial_layer_eccentricity():
    layer = radial_layer_from_ellipse(2.0, 1.0)
    assert abs(layer.eccentricity_K() - 2.0) < 0.05


@pytest.mark.fast
def test_annular_graph_validation_certified_example():
    pkt = example_certified_packet()
    assert validate_annular_graph(pkt)
    assert all(pkt.checks.values())


@pytest.mark.fast
def test_eccentricity_excludes_directive_020_family():
    assert directive_020_falsification_excluded(K_bound=CERTIFIED_REGIME.K)
    audit = audit_thin_ellipse(10.0, 0.5, K_max=CERTIFIED_REGIME.K)
    assert audit.fixed_K_excluded


@pytest.mark.fast
def test_radial_gap_in_certified_regime():
    pkt = example_certified_packet()
    gmin, gmax = radial_gap_ratio(pkt.layers[0], pkt.layers[1])
    assert CERTIFIED_REGIME.g_minus <= gmin <= gmax <= CERTIFIED_REGIME.g_plus


@pytest.mark.fast
def test_corridor_width_check():
    pkt = example_certified_packet()
    assert pkt.corridor_width <= CERTIFIED_REGIME.w_corr


@pytest.mark.fast
def test_normalize_layer_pair_g_star():
    pkt = example_certified_packet()
    pair = normalize_layer_pair(pkt.layers[0], pkt.layers[1])
    assert abs(pair.outer.max_radius() - 1.0) < 1e-9
    assert 0.4 < pair.g_star < 0.5


@pytest.mark.fast
def test_radial_correspondence_cyclic_order():
    pkt = example_certified_packet()
    pair = normalize_layer_pair(pkt.layers[0], pkt.layers[1])
    corr = build_radial_correspondence(pair)
    assert corr.cyclic_order_preserved
    assert corr.orientation_preserving


@pytest.mark.fast
def test_psi_bound_components():
    bound = psi_from_constants(CERTIFIED_REGIME, g_star=0.45)
    assert bound.psi < bound.rho_cyc
    assert bound.sufficient
    assert bound.components["eccentricity"] >= 0.0


@pytest.mark.fast
def test_observed_distance_below_proved_psi():
    pkt = example_certified_packet()
    pair = normalize_layer_pair(pkt.layers[0], pkt.layers[1])
    observed = psi_from_correspondence(pair)
    proved = psi_from_constants(CERTIFIED_REGIME, g_star=pair.g_star).psi
    assert observed <= proved + 1e-9


@pytest.mark.fast
def test_certified_regime_nonempty():
    cert = certify_t036_n1_ann()
    assert cert.in_certified_regime
    assert cert.psi_sufficient
    assert cert.t039_applies
    assert cert.t036_n1_ann_status == "PROVED_LOCALLY"


@pytest.mark.fast
def test_t039_transfer_reference():
    ref = certify_reference_annular()
    assert ref.t039_applies
    assert ref.rank_dg == 3


@pytest.mark.fast
def test_packet_scale_side_bound():
    r_n = 2.5
    assert annular_side_bound(r_n, C_ANN) == pytest.approx(0.3)


@pytest.mark.fast
def test_positive_scale_compactness():
    cor = positive_scale_corollary([0.1, 0.2, 0.15, 0.18], c_ann=C_ANN)
    assert cor.limsup_r_positive
    assert cor.compactness_valid
    assert cor.side_bound_uniform > 0


@pytest.mark.fast
def test_shrinking_scale_no_limit_square():
    cor = positive_scale_corollary([0.01, 0.005, 0.002], c_ann=C_ANN)
    assert not cor.limit_square_exists


@pytest.mark.fast
def test_counterexample_search_no_success():
    assert no_successful_counterexample()
    attempts = search_annular_counterexamples(K_bound=2.0)
    assert len(attempts) >= 3


@pytest.mark.fast
def test_recursive_cross_scale_diagnostic():
    diag = build_concentric_generations(n=4)
    assert len(diag.generations) == 4
    assert not diag.cross_scale_rhombus_candidate


@pytest.mark.fast
def test_reference_certificate_export(tmp_path):
    path = tmp_path / "ref_cert.json"
    data = export_reference_certificate_json(path)
    assert data["t039_applies"]
    assert data["psi_sufficient"]
    assert path.exists()


@pytest.mark.fast
def test_illustration_geometry_consistency():
    """Panel geometry: certified example has K near 1 and four quadrant windows."""
    pkt = example_certified_packet()
    assert pkt.layers[0].eccentricity_K() < 1.01
    pair = normalize_layer_pair(pkt.layers[0], pkt.layers[1])
    corr = build_radial_correspondence(pair)
    assert len(corr.window_points_packet) == 4
    assert corr.max_distance < rho_cyc_reference()
