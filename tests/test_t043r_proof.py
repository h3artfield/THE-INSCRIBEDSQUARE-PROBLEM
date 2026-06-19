"""T043R proof and clean-room audit tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.examples import example_bump_disk, example_bump_polygon
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.t043r_clean_room import run_clean_room_audit
from squarepeg.defect_surgery.t043r_proof import (
    certify_t043r,
    prove_area_tight_from_master,
    prove_area_tight_under_signature,
    prove_uniform_convergence,
)


@pytest.mark.fast
def test_uniform_convergence_bound():
    ok, bound = prove_uniform_convergence(p_to_gamma=True, max_diam=0.01)
    assert ok
    assert bound == 0.01


@pytest.mark.fast
def test_area_tight_master_bound():
    upper = prove_area_tight_from_master(beta=0.005, sigma=0.003, chi=0.0)
    assert upper == pytest.approx(0.008)


@pytest.mark.fast
def test_area_tight_epsilon_delta():
    assert prove_area_tight_under_signature(beta_delta=0.005, sigma_delta=0.005)


@pytest.mark.fast
def test_certify_t043r_bump():
    from squarepeg.defect_surgery.packet_disk import PacketDisk

    small = PacketDisk(center=(1.5, 0.0), radius=0.005, interval_start=1, interval_end=3)
    forest = PacketForest(disks=[small])
    cert = certify_t043r(forest=forest, beta=0.005, sigma=0.005)
    assert cert.status == "PROVED_LOCALLY"
    assert cert.limit_order_correct
    assert cert.t022_applies


@pytest.mark.fast
def test_clean_room_verified():
    audit = run_clean_room_audit(jordan_ok=True)
    assert audit.verdict == "T043R_CLEAN_ROOM_VERIFIED"
    assert all(audit.answers.values())
