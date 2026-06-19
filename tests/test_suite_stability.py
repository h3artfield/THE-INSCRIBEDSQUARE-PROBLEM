"""Full-suite stability baseline (Directive 019)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BASELINE_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "full_suite_baseline.json"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.slow
def test_fast_suite_deterministic_twice():
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "fast", "-q", "--tb=no"]
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    r1 = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=PROJECT_ROOT)
    r2 = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=PROJECT_ROOT)
    assert r1.returncode == 0, r1.stdout + r1.stderr
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert r1.stdout.strip() == r2.stdout.strip()


@pytest.mark.fast
def test_fast_suite_baseline_recorded():
    if not BASELINE_PATH.exists():
        pytest.skip("baseline not yet recorded")
    data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    assert data.get("marker") == "fast"
    assert data.get("exit_code") == 0
