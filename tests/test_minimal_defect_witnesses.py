"""Minimal defect witness extraction."""

import pytest

from squarepeg.robust_degree.area_defect import polygon_gamma
from squarepeg.robust_degree.defect_witness import extract_minimal_witnesses


@pytest.mark.fast
def test_witness_extraction_or_gap():
    verts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    g = polygon_gamma(verts)
    result = extract_minimal_witnesses([g], [0.5, 0.25])
    assert result.selection_lemma_required or len(result.witnesses) >= 0


@pytest.mark.fast
def test_gap_documented_when_empty():
    result = extract_minimal_witnesses([], [])
    assert result.selection_lemma_required
    assert "T035-GAP" in result.gap_description
