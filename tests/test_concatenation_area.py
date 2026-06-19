"""Chen concatenation identity tests."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_surgery.concatenation_area import (
    chen_identity_holds,
    chen_identity_three,
    finite_concatenation_identity,
)


@pytest.mark.fast
def test_chen_three_point():
    s, u, t = (0.0, 0.0), (1.0, 0.0), (1.0, 1.0)
    path_su = [s, u]
    path_ut = [u, t]
    path_st = [s, u, t]
    assert chen_identity_three(s, u, t, path_su, path_ut, path_st)


@pytest.mark.fast
def test_finite_concatenation():
    paths = [[(0, 0), (1, 0), (2, 0)], [(2, 0), (2, 1), (2, 2)]]
    assert chen_identity_holds(paths)


@pytest.mark.fast
def test_concatenation_reconstruction():
    paths = [[(0, 0), (1, 0)], [(1, 0), (1, 1), (2, 1)]]
    dec = finite_concatenation_identity(paths)
    assert abs(dec.total - dec.reconstructed) < 1e-8
