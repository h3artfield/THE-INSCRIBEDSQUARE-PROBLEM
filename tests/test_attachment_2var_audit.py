"""Attachment (2)-variation audit tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.attachment_2var_audit import (
    attachment_2var_verdict,
    circle_chord_2var_counterexample,
    simple_chain_t021_bound,
)


@pytest.mark.fast
def test_2var_requires_extra_structure():
    audit = circle_chord_2var_counterexample(128)
    assert audit.verdict == "ATTACHMENT_2VAR_REQUIRES_EXTRA_STRUCTURE"
    assert audit.counterexample_consecutive_v2_to_zero
    assert audit.counterexample_area_persists


@pytest.mark.fast
def test_simple_chain_t021():
    assert simple_chain_t021_bound([(0, 0), (1, 0), (1, 1)])


@pytest.mark.fast
def test_verdict_literal():
    assert attachment_2var_verdict(128) == "ATTACHMENT_2VAR_REQUIRES_EXTRA_STRUCTURE"
