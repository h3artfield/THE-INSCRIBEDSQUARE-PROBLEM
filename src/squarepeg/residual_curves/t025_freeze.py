"""Generate frozen T025/T027 artifacts for Directive 013."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from squarepeg.residual_curves.c0_square_perturbation import build_c0_certificate
from squarepeg.residual_curves.independent_t025_verifier import (
    build_smooth_square_certificate_json,
    replay_t025_certificate,
    verifier_hash,
)
from squarepeg.residual_curves.square_boundary_degree import (
    boundary_certificate_hash,
    certify_boundary_exclusion,
    validate_boundary_certificate,
)
from squarepeg.residual_curves.t025_frozen_constants import (
    CANONICAL_CURVE_HASH,
    INTERVAL_LIBRARY,
    KRAWCZYK_THETA_BOXES,
    ROUNDING_MODE,
    T025_STATUS,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _git_head() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=_repo_root(), text=True
        )
        return out.strip()
    except Exception:
        return "unknown"


def write_artifacts() -> dict:
    root = _repo_root()
    art = root / "artifacts"
    art.mkdir(exist_ok=True)

    replay = replay_t025_certificate()
    smooth_cert = build_smooth_square_certificate_json()
    smooth_path = art / "t025_smooth_square_certificate.json"
    with open(smooth_path, "w", encoding="utf-8") as f:
        json.dump(smooth_cert, f, indent=2, sort_keys=True)
    smooth_hash = hashlib.sha256(smooth_path.read_bytes()).hexdigest()

    bnd_cert = certify_boundary_exclusion(max_depth=6)
    bnd_valid = validate_boundary_certificate(bnd_cert)
    bnd_payload = bnd_cert.to_dict()
    bnd_payload["certificate_hash_sha256"] = boundary_certificate_hash(bnd_cert)
    bnd_payload["independent_validation_passed"] = bnd_valid
    bnd_path = art / "t025_boundary_exclusion_certificate.json"
    with open(bnd_path, "w", encoding="utf-8") as f:
        json.dump(bnd_payload, f, indent=2, sort_keys=True)

    c0 = build_c0_certificate(bnd_cert.boundary_margin)

    test_out = subprocess.check_output(
        [sys.executable, "-m", "pytest", "tests/test_t025_certificate_replay.py", "-q"],
        cwd=root,
        text=True,
        stderr=subprocess.STDOUT,
    )

    manifest = {
        "directive": "013",
        "tag": "t025-smooth-double-spiral-internal-2026-06-18",
        "commit_hash": _git_head(),
        "canonical_curve_hash_sha256": CANONICAL_CURVE_HASH,
        "interval_library": INTERVAL_LIBRARY,
        "arithmetic_precision": "float64_outward_enclosure",
        "rounding_mode": ROUNDING_MODE,
        "root_box_endpoints": [[str(a), str(b)] for a, b in KRAWCZYK_THETA_BOXES],
        "krawczyk_matrix": smooth_cert["jacobian_at_center"],
        "krawczyk_inclusion_result": smooth_cert["krawczyk_image_in_interior"],
        "side_length_bound": smooth_cert["side_length_bounds"],
        "radius_bound": smooth_cert["radial_lower_bounds"],
        "certificate_hash_sha256": smooth_hash,
        "independent_validator_hash_sha256": verifier_hash(),
        "t025_status": T025_STATUS,
        "replay_verdict": replay.status,
        "boundary_margin": bnd_cert.boundary_margin,
        "degree": bnd_cert.degree,
        "eta0": c0.eta0,
        "t027_homotopy_ok": c0.homotopy_boundary_excluded,
        "test_output": test_out.strip(),
    }
    manifest_path = art / "t025_verified_internal_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    review = root / "review"
    review.mkdir(exist_ok=True)
    review_cert = review / "T025_machine_certificate.json"
    review_cert.write_text(smooth_path.read_text(encoding="utf-8"), encoding="utf-8")

    return {
        "replay": replay.status,
        "boundary_valid": bnd_valid,
        "eta0": c0.eta0,
        "manifest": str(manifest_path),
    }


if __name__ == "__main__":
    print(json.dumps(write_artifacts(), indent=2))
