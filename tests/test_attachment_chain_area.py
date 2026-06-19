"""Attachment chain area tests."""

from __future__ import annotations

import math

import pytest

from squarepeg.defect_surgery.attachment_chain import (
    attachment_chain_area,
    build_chord_chain_from_disks,
    v_att2_squared,
)
from squarepeg.defect_surgery.attachment_chain import AttachmentChain
from squarepeg.defect_surgery.examples import example_bump_disk, example_bump_polygon


@pytest.mark.fast
def test_attachment_chain_area_nontrivial():
    n = 32
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    chain = AttachmentChain(points=pts, chord_indices=list(range(len(pts))))
    assert abs(attachment_chain_area(chain)) > 0.01


@pytest.mark.fast
def test_v_att2_positive():
    chain = AttachmentChain(points=[(0, 0), (1, 0), (1, 1)], chord_indices=[1, 2])
    assert v_att2_squared(chain) > 0


@pytest.mark.fast
def test_build_chord_chain():
    verts = example_bump_polygon()
    chain = build_chord_chain_from_disks(verts, [example_bump_disk()])
    assert len(chain.points) >= 2
