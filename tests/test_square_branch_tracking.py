"""Tests for square branch tracking on truncations."""

import pytest

from squarepeg.residual_curves.limit_square import build_compactness_certificate
from squarepeg.residual_curves.square_branch_tracking import (
    branch_continuation_report,
    stable_outer_branch,
)


@pytest.mark.fast
def test_stable_outer_branch_exists():
    from squarepeg.residual_curves.square_branch_tracking import analyze_truncation, macroscopic_branch_filter
    recs = analyze_truncation(3)
    macro = [r for r in recs if macroscopic_branch_filter(r)]
    assert len(macro) >= 1
    assert macro[0].side_over_diameter >= 0.45


@pytest.mark.fast
def test_compactness_certificate():
    cert = build_compactness_certificate(turn_min=3, turn_max=4)
    assert cert.certification_status == "certified"
    assert cert.min_side_over_diameter >= 0.45


@pytest.mark.slow
def test_stable_branch_multi_turn():
    branches = stable_outer_branch(range(3, 6))
    assert len(branches) >= 1


@pytest.mark.slow
def test_branch_report():
    report = branch_continuation_report(turns_max=5)
    assert report["stable_count"] >= 1
    assert report["best_side_over_diameter"] >= 0.45
