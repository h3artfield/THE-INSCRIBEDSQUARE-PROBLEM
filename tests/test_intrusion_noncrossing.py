"""Directive 028 — intrusion noncrossing tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.intrusion_noncrossing import (
    IntrusionComponent,
    audit_noncrossing,
    classify_endpoint_order,
)


@pytest.mark.fast
def test_nested_endpoints_compatible():
    order = classify_endpoint_order((0, 0), (1, 0), (0.2, 0.1), (0.8, 0.1))
    assert order in ("NESTED", "SEPARATED")


@pytest.mark.fast
def test_interleaving_endpoints_incompatible():
    order = classify_endpoint_order((0, 0), (0.5, 0), (0.3, 0), (0.8, 0))
    assert order == "INTERLEAVING"


@pytest.mark.fast
def test_noncrossing_audit():
    c1 = IntrusionComponent("K1", (0.1, 0.2), (0, 0), (1, 0), False, False, [])
    c2 = IntrusionComponent("K2", (0.3, 0.4), (0.2, 0.1), (0.8, 0.1), False, False, [])
    audit = audit_noncrossing([c1, c2])
    assert audit.compatible
    assert audit.endpoint_order == "NESTED"
