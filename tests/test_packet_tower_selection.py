"""Packet tower selection (T040) tests."""

from __future__ import annotations

import pytest

from squarepeg.defect_geometry.packet_tower_selection import (
    PacketRecord,
    extract_tower_from_packets,
)


@pytest.mark.fast
def test_coherent_extraction():
    records = [
        PacketRecord("p0", (0, 0), 1.0, 0.0, 3.14, 1),
        PacketRecord("p1", (0, 0), 0.45, 0.0, 3.14, 1, "p0"),
        PacketRecord("p2", (0, 0), 0.20, 0.0, 3.14, 1, "p1"),
    ]
    r = extract_tower_from_packets(records)
    assert r.classification == "COHERENT_TOWER_EXTRACTED"
    assert r.coherent


@pytest.mark.fast
def test_center_drift_obstruction():
    records = [
        PacketRecord("p0", (0, 0), 1.0, 0.0, 3.14, 1),
        PacketRecord("p1", (0.5, 0), 0.3, 0.0, 3.14, 1, "p0"),
    ]
    r = extract_tower_from_packets(records)
    assert r.classification == "CENTER_DRIFT_OBSTRUCTION"


@pytest.mark.fast
def test_branching_tree():
    records = [
        PacketRecord("p0", (0, 0), 1.0, 0.0, 3.14, 1),
        PacketRecord("p1a", (0, 0), 0.45, 0.0, 3.14, 1, "p0"),
        PacketRecord("p1b", (0, 0), 0.40, 0.0, 3.14, 1, "p0"),
    ]
    r = extract_tower_from_packets(records)
    assert r.classification == "BRANCHING_DEFECT_TREE"
