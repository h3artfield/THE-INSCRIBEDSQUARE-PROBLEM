"""Tests for protected annuli."""

import math

import pytest

from squarepeg.residual_curves.protected_annuli import (
    annuli_pairwise_disjoint,
    annulus_for_turn,
    protected_annuli_for_turns,
)


@pytest.mark.fast
def test_annuli_disjoint_for_even_turns():
    annuli = protected_annuli_for_turns(8, even_only=True)
    assert len(annuli) == 4
    assert annuli_pairwise_disjoint(annuli)


@pytest.mark.fast
def test_protected_subannulus_inside_outer():
    ann = annulus_for_turn(2)
    assert ann.protected.inner > ann.outer.inner
    assert ann.protected.outer < ann.outer.outer
    assert ann.min_arm_separation > 0
