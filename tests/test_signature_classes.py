"""Practical signature class tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.attachment_chain import AttachmentChain
from squarepeg.defect_surgery.bounded_multiplicity_signature import audit_bounded_multiplicity_signature
from squarepeg.defect_surgery.bounded_winding_signature import audit_bounded_winding_signature
from squarepeg.defect_surgery.examples import example_bump_disk, example_bump_polygon
from squarepeg.defect_surgery.exact_component_decomposition import decompose_cyclic_interval
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.simple_signature import simple_signature_implies_sigma


@pytest.mark.fast
def test_simple_signature_l_path():
    chain = AttachmentChain(points=[(0, 0), (1, 0), (1, 1)], chord_indices=[1])
    audit = simple_signature_implies_sigma(chain, v2_threshold=10.0)
    assert audit.chain_is_simple
    assert audit.implies_signature_sigma


@pytest.mark.fast
def test_bounded_multiplicity_bump():
    forest = PacketForest(disks=[example_bump_disk()])
    decomp = decompose_cyclic_interval(example_bump_polygon(), 0, 3, forest)
    audit = audit_bounded_multiplicity_signature(
        forest.disks, decomp.components, set(range(4)), max_multiplicity=3, max_diam=1.0
    )
    assert audit.multiplicity == 1
    assert audit.sigma_bound > 0


@pytest.mark.fast
def test_bounded_winding_small():
    chain = AttachmentChain(points=[(0, 0), (0.01, 0), (0.01, 0.01), (0, 0.01)], chord_indices=[])
    audit = audit_bounded_winding_signature(chain, max_wind=2, diameter=0.02)
    assert audit.bound_holds
