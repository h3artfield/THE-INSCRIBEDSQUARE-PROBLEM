"""Uniform truncation margin tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_geometry.tower_cyclic_certificate import (
    U_TOWER,
    certify_reference_tower,
    uniform_truncation_margins,
)


@pytest.mark.fast
def test_packet_level_uniform_margins():
    m_g, side, sep = uniform_truncation_margins()
    assert m_g > 0
    assert side >= U_TOWER["side_fraction_r1"]
    assert sep >= U_TOWER["sep_fraction_r1"]


@pytest.mark.fast
def test_reference_tower_jordan_certified():
    cert = certify_reference_tower()
    assert cert.jordan_audit_pass
    assert cert.packet_level_t039
    assert cert.uniform_margins
    assert cert.status == "REFERENCE_JORDAN_CERTIFIED"
    assert not cert.cross_scale_fixed_support
