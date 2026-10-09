"""Frozen D042–D061 certificate snapshot consistency (tier 2 audit)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from squarepeg.ledger.frozen_certificate_snapshot import (
    DIRECTIVE_RANGE,
    SNAPSHOT_PATH,
    load_manifest,
    load_snapshot,
    manifest_path,
)

ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts"


@pytest.mark.audit
def test_snapshot_file_exists():
    assert SNAPSHOT_PATH.exists()


@pytest.mark.audit
def test_snapshot_covers_d042_d061():
    snap = load_snapshot()
    assert snap["frozen_through_directive"] == 61
    for n in DIRECTIVE_RANGE:
        assert str(n) in snap["directives"]


@pytest.mark.audit
def test_manifests_present_through_d060():
    for n in range(42, 61):
        assert manifest_path(n).exists(), f"missing manifest for D{n:03d}"


@pytest.mark.audit
def test_snapshot_matches_manifests():
    snap = load_snapshot()
    for n in range(42, 61):
        m = load_manifest(n)
        entry = snap["directives"][str(n)]
        assert entry["manifest_present"]
        assert entry["outcome"] == m.get("outcome")
        proof = entry.get("proof_commit_hash")
        mproof = m.get("proof_commit_hash") or m.get("commit_hash")
        if proof and mproof:
            assert proof.startswith(mproof[:7]) or mproof.startswith(str(proof)[:7])


@pytest.mark.audit
def test_t045r_conjectural_everywhere():
    snap = load_snapshot()
    assert snap["global_invariants"]["T045R"] == "CONJECTURAL_FULL_EXTRACTION"
    for n in DIRECTIVE_RANGE:
        ts = snap["directives"][str(n)].get("theorem_status") or {}
        if "T045R" in ts:
            assert ts["T045R"] == "CONJECTURAL_FULL_EXTRACTION"


@pytest.mark.audit
def test_singleton_cantor_not_reintroduced():
    snap = load_snapshot()
    removed = snap["global_invariants"]["removed_independent_residuals"]
    assert "NONCARLESON_SINGLETON_CANTOR_END_TANGENT" in removed


@pytest.mark.audit
def test_baseline_regression_recorded():
    snap = load_snapshot()
    base = snap["last_verified_full_regression"]
    assert base["passed"] == 303
    assert base["failed"] == 0
    assert base["exit_code"] == 0


@pytest.mark.audit
def test_milestone_target_includes_d061():
    snap = load_snapshot()
    target = snap["milestone_regression_target"]
    assert target["expected_passed"] == 314


@pytest.mark.audit
def test_regression_tier_definitions():
    snap = load_snapshot()
    tiers = snap["regression_tiers"]
    for key in ("tier1_new_directive", "tier2_audit", "tier3_deep_sample", "tier4_milestone"):
        assert key in tiers
        assert "marker" in tiers[key]
        assert "description" in tiers[key]


@pytest.mark.audit
def test_d060_frozen_baseline_commits():
    snap = load_snapshot()
    assert snap["baseline_manifest_commit"] == "069c792"
    assert snap["baseline_proof_commit"] == "a2899d5"


@pytest.mark.audit
def test_d061_provisional_entry():
    snap = load_snapshot()
    d61 = snap["directives"]["61"]
    assert d61.get("provisional") is True
    assert d61["clean_room"] == "D061_CLEAN_ROOM_VERIFIED"
    assert d61["fast_tests"]["passed"] == 11
