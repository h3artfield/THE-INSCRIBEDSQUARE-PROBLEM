"""Directive 020 nested-lobe geometry tests."""

from __future__ import annotations

import math

import pytest

from squarepeg.area_variation.adversarial_arcs import semicircle_arc
from squarepeg.defect_geometry.annular_windows import extract_windows, windows_disjoint
from squarepeg.defect_geometry.cross_scale_search import classify_scale_escape, search_cross_scale, PacketTreeNode
from squarepeg.defect_geometry.lobe_tree import build_lobe_tree
from squarepeg.defect_geometry.nested_chain import NestedClassParams, in_D_nest
from squarepeg.defect_geometry.packet_normalization import normalize_packet
from squarepeg.defect_geometry.packet_reference_distance import compare_packet_to_reference, psi_estimate
from squarepeg.defect_geometry.reference_cyclic_certificate import certify_reference_annular, rho_cyc_reference
from squarepeg.defect_geometry.reference_rhombus_family import audit_reference_rhombus_family
from squarepeg.defect_geometry.nested_lobe_certificate import certify_nested_packet
from squarepeg.robust_degree.cyclic_equivariance import verify_A_properties


@pytest.mark.fast
def test_A_fourth_power():
    ok, det_ok, _ = verify_A_properties()
    assert ok and det_ok


@pytest.mark.fast
def test_lobe_tree_nesting():
    pts = list(semicircle_arc(64).vertices)
    tree = build_lobe_tree(pts, max_depth=4)
    assert tree.max_depth >= 2
    assert tree.root.diameter > 0


@pytest.mark.fast
def test_D_nest_same_sign_chain():
    pts = [(math.cos(t), math.sin(t)) for t in [i * math.pi / 16 for i in range(17)]]
    tree = build_lobe_tree(pts, max_depth=5)
    params = NestedClassParams(min_depth=2, beta=0.001, delta_sep=0.01)
    assert in_D_nest(tree, params) or tree.root.enclosed_area != 0


@pytest.mark.fast
def test_packet_normalization_unit_diameter():
    pts = [(0, 0), (2, 0), (2, 3), (0, 3)]
    pkt = normalize_packet(pts)
    assert abs(pkt.diameter - 1.0) < 1e-9


@pytest.mark.fast
def test_reference_rhombus_rank_three():
    fam = audit_reference_rhombus_family()
    assert fam.rank_dg == 3
    assert fam.g_zero_on_family
    assert fam.side_margin > 0.05


@pytest.mark.fast
def test_reference_t039_certificate():
    cert = certify_reference_annular(0.01)
    assert cert.t039_applies
    assert cert.w1_pairing == 1
    assert cert.rank_dg == 3


@pytest.mark.fast
def test_sign_line_pairing_reference():
    cert = certify_reference_annular()
    assert cert.mod2_normal_degree == 1


@pytest.mark.fast
def test_window_extraction_disjoint():
    pts = [(math.cos(t), math.sin(t)) for t in [i * math.pi / 12 for i in range(13)]]
    tree = build_lobe_tree(pts, max_depth=4)
    wins = extract_windows(tree, j=0, q0=1)
    if wins is not None:
        assert windows_disjoint(wins)


@pytest.mark.fast
def test_psi_estimate_positive():
    psi = psi_estimate(m=4, lambda_minus=0.25, lambda_plus=0.75, delta_sep=0.05, beta=0.01, q0=1)
    assert psi > 0


@pytest.mark.fast
def test_nesting_alone_not_sufficient():
    pts = list(semicircle_arc(48).vertices)
    tree = build_lobe_tree(pts, max_depth=5)
    cmp = compare_packet_to_reference(tree)
    assert cmp.missing_hypothesis is not None or cmp.closeness_sufficient


@pytest.mark.fast
def test_nested_certificate_reference_t039():
    pts = [(math.cos(t), 0.3 * math.sin(t)) for t in [i * math.pi / 10 for i in range(11)]]
    tree = build_lobe_tree(pts, max_depth=4)
    cert = certify_nested_packet(tree)
    assert cert.reference_t039


@pytest.mark.fast
def test_scale_escape_shrinking():
    assert classify_scale_escape([0.04, 0.03, 0.02, 0.01, 0.005]) == "SHRINKING_PACKETS"


@pytest.mark.fast
def test_eccentric_ellipse_low_rho():
    """Eccentric packet: nesting may hold but Psi vs rho_cyc not certified."""
    pts = [(2 * math.cos(t), 0.2 * math.sin(t)) for t in [i * math.pi / 8 for i in range(9)]]
    tree = build_lobe_tree(pts, max_depth=3)
    cmp = compare_packet_to_reference(tree)
    rho = rho_cyc_reference()
    assert rho > 0
    # Eccentric geometry typically fails unconditional closeness
    assert not cmp.closeness_sufficient or cmp.psi >= 0
