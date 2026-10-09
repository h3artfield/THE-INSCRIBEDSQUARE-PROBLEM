"""Regression tier helpers (Directive certificate snapshots)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from squarepeg.ledger.frozen_certificate_snapshot import (
    DEEP_SAMPLE_TEST_FILES,
    MILESTONE_TEST_FILES,
    regression_tiers,
    write_snapshot,
)

ROOT = Path(__file__).resolve().parents[3]


def run_tier(tier_name: str, extra: list[str] | None = None) -> int:
    tier = next(t for t in regression_tiers() if t.name == tier_name)
    cmd = [sys.executable, "-m", "pytest", *tier.pytest_args, "-q", "--tb=line"]
    if tier_name == "tier1_new_directive" and extra:
        cmd.extend(extra)
    elif tier_name in ("tier3_deep_sample", "tier4_milestone"):
        pass
    elif tier_name == "tier2_audit":
        cmd.append("tests/test_frozen_certificate_snapshot.py")
    if extra and tier_name != "tier1_new_directive":
        cmd.extend(extra)
    return subprocess.call(cmd, cwd=ROOT)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run regression tier for frozen certificate snapshots")
    parser.add_argument("tier", choices=[t.name for t in regression_tiers()] + ["refresh_snapshot"])
    parser.add_argument("tests", nargs="*", help="For tier1: test file(s), e.g. tests/test_directive_061.py")
    args = parser.parse_args()
    if args.tier == "refresh_snapshot":
        p = write_snapshot()
        print(f"Wrote {p}")
        return
    extra = list(args.tests) if args.tests else None
    if args.tier == "tier1_new_directive" and not extra:
        print("tier1 requires test file: tests/test_directive_NNN.py")
        sys.exit(2)
    sys.exit(run_tier(args.tier, extra))


if __name__ == "__main__":
    main()
