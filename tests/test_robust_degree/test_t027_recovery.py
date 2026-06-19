"""Recover T025/T027 via abstract framework."""

import pytest

from squarepeg.robust_degree.limit_persistence import recover_t027_instance


@pytest.mark.fast
def test_t027_recovery():
    result = recover_t027_instance()
    assert result.rho > 0
    assert result.allowed_perturbation > 0
    assert result.square_exists
