"""Directive 028 — saturation order independence."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.intrusion_noncrossing import IntrusionComponent
from squarepeg.defect_extraction.saturation import recursive_saturation, saturation_order_independent


def _intrusions():
    return [
        IntrusionComponent("K1", (0.55, 0.72), (1.2, 0.1), (1.8, 0.1), False, False, ["K2"]),
        IntrusionComponent("K2", (0.6, 0.65), (1.3, 0.15), (1.7, 0.15), False, False, []),
    ]


@pytest.mark.fast
def test_saturation_stabilizes():
    state = recursive_saturation((0.15, 0.45), _intrusions())
    assert state.stabilized
    assert len(state.param_intervals) >= 1


@pytest.mark.fast
def test_saturation_order_independent():
    assert saturation_order_independent((0.15, 0.45), _intrusions())
