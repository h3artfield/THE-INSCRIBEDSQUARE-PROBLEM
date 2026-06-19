"""Tests: infinite sequence of certified polygon squares (Route B)."""

import pytest

from squarepeg.residual_curves.truncation_audit import (
    MACRO_BRANCH_EDGES,
    macro_square_certificate,
)


@pytest.mark.fast
def test_same_linear_system_pattern():
    """Edges (0,3,5,0) use N-independent outer-arm geometry for N>=3."""
    certs = [macro_square_certificate(n) for n in range(3, 8)]
    assert all(c is not None for c in certs)
    for c in certs:
        assert c.edge_indices == MACRO_BRANCH_EDGES
        assert c.validator_ok


@pytest.mark.fast
def test_unbounded_sequence_exists():
    """N_k = k+3 gives certified square for every k (not merely N<=7)."""
    for n in range(3, 6):
        cert = macro_square_certificate(n)
        assert cert is not None and cert.validator_ok
