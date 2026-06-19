"""Square mass sufficiency tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.square_mass_counterexample import (
    circle_chord_chain_counterexample,
    counterexample_sequence,
    square_mass_sufficiency_verdict,
)


@pytest.mark.fast
def test_square_mass_insufficient():
    assert square_mass_sufficiency_verdict(128) == "SQUARE_MASS_INSUFFICIENT"


@pytest.mark.fast
def test_mu2_vanishes_attachment_persists():
    ex = circle_chord_chain_counterexample(128)
    assert ex.mu2 < 1.0
    assert ex.attachment_area > 0.1


@pytest.mark.fast
def test_counterexample_sequence():
    seq = counterexample_sequence(256)
    assert seq[-1].mu2 < seq[0].mu2
