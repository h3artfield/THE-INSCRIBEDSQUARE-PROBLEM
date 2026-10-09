"""Universal proof obligation audit tests."""

from __future__ import annotations

import pytest

from squarepeg.ledger.universal_proof_obligations import list_universal_obligations, universal_theorem_closed


@pytest.mark.audit
def test_obligations_listed():
    obs = list_universal_obligations()
    assert len(obs) >= 8
    tracks = {o.track for o in obs}
    assert "A_MICROLICAL" in tracks
    assert "B_EXTRACTION" in tracks
    assert "C_TOEPLITZ" in tracks


@pytest.mark.audit
def test_toeplitz_still_open():
    assert not universal_theorem_closed()
    c1 = next(o for o in list_universal_obligations() if o.id == "C1")
    assert c1.status == "OPEN"
