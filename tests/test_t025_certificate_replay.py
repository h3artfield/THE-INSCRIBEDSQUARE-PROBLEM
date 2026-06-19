"""Tests for independent T025 certificate replay."""

import json
from pathlib import Path

import pytest

from squarepeg.residual_curves.independent_t025_verifier import (
    build_smooth_square_certificate_json,
    replay_t025_certificate,
)
from squarepeg.residual_curves.t025_frozen_constants import T025_STATUS


@pytest.mark.fast
def test_replay_verdict():
    replay = replay_t025_certificate()
    assert replay.status == "T025_CERTIFICATE_REPLAYED"
    assert replay.passed
    assert replay.det_sign != 0
    assert replay.side_lb >= 0.35
    assert replay.radius_lb >= 0.2


@pytest.mark.fast
def test_frozen_certificate_json():
    cert = build_smooth_square_certificate_json()
    assert cert["status"] == T025_STATUS
    assert cert["replay_verdict"] == "T025_CERTIFICATE_REPLAYED"
    assert len(cert["F_interval_enclosure"]) == 4
    assert cert["krawczyk_image_in_interior"] or cert["numerical_center_optional"]

    root = Path(__file__).resolve().parents[1]
    path = root / "artifacts" / "t025_smooth_square_certificate.json"
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8"))
        assert loaded["replay_verdict"] == "T025_CERTIFICATE_REPLAYED"
