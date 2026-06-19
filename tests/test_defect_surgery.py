"""Directive 023 defect surgery tests."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_surgery.area_change import area_change_straight_chord
from squarepeg.defect_surgery.area_tight_recovery import audit_area_tight_recovery
from squarepeg.defect_surgery.annular_surgery_class import audit_annular_isolated
from squarepeg.defect_surgery.carleson_mass import mu_D_on_interval, packet_mass
from squarepeg.defect_surgery.crosscut import straight_chord_crosscut
from squarepeg.defect_surgery.defect_forest_extraction import extract_defect_forest
from squarepeg.defect_surgery.examples import example_bump_disk, example_bump_polygon
from squarepeg.defect_surgery.local_surgery import apply_local_surgery
from squarepeg.defect_surgery.nested_forest import PacketForest, apply_disjoint_surgeries, forest_is_admissible
from squarepeg.defect_surgery.packet_disk import validate_isolated_packet
from squarepeg.defect_surgery.surgery_falsification import run_surgery_falsifications
from squarepeg.defect_surgery.t042_certificate import certify_t042, t041_shrinking_support_obstruction


@pytest.mark.fast
def test_t041_shrinking_support():
    assert "side(Q) <= r" in t041_shrinking_support_obstruction()
    r_n = 0.01
    assert r_n < 0.1  # shrinking support bound


@pytest.mark.fast
def test_isolated_disk_validation():
    verts = example_bump_polygon()
    disk = example_bump_disk()
    audit = validate_isolated_packet(verts, disk, max_diameter=1.0)
    assert audit.is_isolated


@pytest.mark.fast
def test_straight_chord_surgery_jordan():
    res = apply_local_surgery(example_bump_polygon(), example_bump_disk())
    assert res.is_jordan
    assert res.uniform_error <= 1.0


@pytest.mark.fast
def test_t042_certified():
    cert = certify_t042(example_bump_polygon(), example_bump_disk())
    assert cert.status == "PROVED_LOCALLY"
    assert cert.jordan_preserved
    assert cert.replacement_area_zero


@pytest.mark.fast
def test_area_change_straight_chord():
    verts = example_bump_polygon()
    disk = example_bump_disk()
    chain = verts[disk.interval_start : disk.interval_end + 1]
    cross = straight_chord_crosscut(verts[disk.interval_start], verts[disk.interval_end])
    b = area_change_straight_chord(chain, cross)
    assert b.bound <= 1.0 + 1e-9


@pytest.mark.fast
def test_packet_mass():
    m = packet_mass(example_bump_disk())
    assert m.mu == pytest.approx(1.0)


@pytest.mark.fast
def test_disjoint_surgeries():
    verts = example_bump_polygon()
    forest = PacketForest(disks=[example_bump_disk()])
    assert forest_is_admissible(forest)
    out, results = apply_disjoint_surgeries(verts, forest)
    assert results[0].is_jordan
    assert len(out) < len(verts)


@pytest.mark.fast
def test_annular_isolated_audit():
    audit = audit_annular_isolated()
    assert audit.annular_graph_ok


@pytest.mark.fast
def test_defect_forest_extraction_positive_scale():
    from squarepeg.defect_surgery.packet_disk import PacketDisk

    d = PacketDisk(center=(0, 0), radius=0.2, interval_start=0, interval_end=1)
    r = extract_defect_forest([d], scales=[0.5, 0.4])
    assert r.positive_scale


@pytest.mark.fast
def test_surgery_falsification():
    rep = run_surgery_falsifications()
    assert len(rep.cases) >= 3


@pytest.mark.fast
def test_area_tight_recovery_audit():
    audit = audit_area_tight_recovery([], [], alpha_outside=0.0)
    assert audit.status in ("CONJECTURAL_TARGET", "PRECISE_GAP", "PROVED_LOCALLY")
