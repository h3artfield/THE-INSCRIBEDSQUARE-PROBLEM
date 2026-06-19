"""Attachment signature moduli tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.attachment_signature import (
    alpha_bound_holds,
    moduli_from_decomposition,
    verify_beta_noncircular,
    verify_sigma_noncircular,
)
from squarepeg.defect_surgery.examples import example_bump_disk, example_bump_polygon
from squarepeg.defect_surgery.exact_component_decomposition import decompose_cyclic_interval
from squarepeg.defect_surgery.nested_forest import PacketForest


@pytest.mark.fast
def test_moduli_noncircular():
    decomp = decompose_cyclic_interval(
        example_bump_polygon(), 0, 6, PacketForest(disks=[example_bump_disk()])
    )
    assert verify_beta_noncircular(decomp)
    assert verify_sigma_noncircular(decomp)
    assert alpha_bound_holds(decomp)


@pytest.mark.fast
def test_moduli_exact_equality():
    decomp = decompose_cyclic_interval(
        example_bump_polygon(), 0, 6, PacketForest(disks=[example_bump_disk()])
    )
    m = moduli_from_decomposition(decomp)
    assert abs(m.alpha - (m.beta + m.sigma + m.chi)) < 1e-8
