"""Generate T025/T027 combined freeze manifest for Directive 014."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=_repo_root(), text=True
        ).strip()
    except Exception:
        return "unknown"


def _file_hash(path: Path) -> str:
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest() -> dict:
    root = _repo_root()
    art = root / "artifacts"
    t025 = json.loads((art / "t025_verified_internal_manifest.json").read_text(encoding="utf-8"))
    bnd_path = art / "t025_boundary_exclusion_certificate.json"
    bnd = json.loads(bnd_path.read_text(encoding="utf-8")) if bnd_path.exists() else {}

    test_out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_robust_degree",
            "tests/test_t025_certificate_replay.py",
            "tests/test_t027_robustness_certificate.py",
            "-q",
        ],
        cwd=root,
        text=True,
        stderr=subprocess.STDOUT,
    )

    manifest = {
        "directive": "014",
        "tag": "t025-t027-robust-square-internal-2026-06-18",
        "commit_hash": _git_head(),
        "canonical_curve_hash_sha256": t025["canonical_curve_hash_sha256"],
        "root_certificate_hash_sha256": t025.get("certificate_hash_sha256"),
        "boundary_cover_hash_sha256": bnd.get("certificate_hash_sha256", _file_hash(bnd_path)),
        "independent_replay_hash_sha256": t025.get("independent_validator_hash_sha256"),
        "eta0": t025.get("eta0"),
        "degree_sign": t025.get("degree"),
        "side_length_bounds": t025.get("side_length_bound"),
        "separation_note": "pairwise LB >= 0.335 on canonical B",
        "t025_status": "PROVED_LOCALLY_BY_DIRECT_INTERVAL_CERTIFICATE",
        "t027_status": "PROVED_LOCALLY_CLEAN_ROOM_VERIFIED",
        "t028_status": "PROVED_AS_COROLLARY",
        "t029_status": "PROVED_LOCALLY",
        "t030_status": "PROVED_LOCALLY",
        "t031_status": "PROVED_LOCALLY",
        "t032_status": "CONJECTURAL_FULL_BRIDGE",
        "t033_status": "FINITE_SCALE_DICHOTOMY_TARGET",
        "directive_014_outcome": "E_DIAGNOSTIC_REDUCTION",
        "test_output": test_out.strip(),
    }
    out = art / "t025_t027_verified_internal_manifest.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(write_manifest(), indent=2))
