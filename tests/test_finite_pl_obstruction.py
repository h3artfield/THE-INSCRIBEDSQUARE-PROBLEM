"""Tests for finite-PL obstruction lemma."""

from fractions import Fraction

import pytest

from squarepeg.spectral_axioms.pl_obstruction import StrictPLFunction, finite_pl_obstruction_holds


@pytest.mark.fast
def test_obstruction_interior_segment():
    g = StrictPLFunction(
        [
            (Fraction(0), Fraction(0)),
            (Fraction(1, 2), Fraction(1, 4)),
            (Fraction(1), Fraction(1)),
        ]
    )
    assert finite_pl_obstruction_holds(g)
    assert g.D_plus_lower_bound() == Fraction(1)  # breakpoint avg (1/2+3/2)/2


@pytest.mark.fast
def test_obstruction_at_breakpoint():
    g = StrictPLFunction(
        [
            (Fraction(0), Fraction(0)),
            (Fraction(1, 2), Fraction(1, 4)),
            (Fraction(1), Fraction(3, 4)),
        ]
    )
    kind, slope = g.slope_at_half()
    assert kind == "breakpoint"
    assert slope == Fraction(3, 4)  # (m_L=1/2 + m_R=1)/2
    assert finite_pl_obstruction_holds(g)


@pytest.mark.fast
def test_flat_segment_not_strict():
    from squarepeg.spectral_axioms.continuum_cells import PLFunction

    pl = PLFunction(
        [
            (Fraction(0), Fraction(0)),
            (Fraction(1, 2), Fraction(0)),
            (Fraction(1), Fraction(1)),
        ]
    )
    assert not all(s.slope > 0 for s in pl.segments)
    assert pl.segments[0].slope == 0
