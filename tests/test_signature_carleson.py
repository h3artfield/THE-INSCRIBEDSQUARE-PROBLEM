"""SIGNATURE_CARLESON tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_surgery.signature_carleson import audit_signature_carleson, version_implies_signature


@pytest.mark.fast
def test_signature_requires_attachment_control():
    bad = audit_signature_carleson(
        max_diam=0.01, disjoint=True, chord_safe=True, beta=0.001, a_att_sup=0.5
    )
    assert not bad.satisfies_signature


@pytest.mark.fast
def test_signature_passes_when_controlled():
    good = audit_signature_carleson(
        max_diam=0.01, disjoint=True, chord_safe=True, beta=0.001, a_att_sup=0.001
    )
    assert good.satisfies_signature


@pytest.mark.fast
def test_version_b_implies_signature():
    assert version_implies_signature("B_att2_variation") is None
