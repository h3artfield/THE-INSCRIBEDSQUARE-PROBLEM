"""Audit square-variable vs boundary parameter order."""

import pytest

from squarepeg.residual_curves.independent_t025_verifier import boundary_order_ok
from squarepeg.residual_curves.t025_frozen_constants import KRAWCZYK_THETA_BOXES


@pytest.mark.fast
def test_boundary_cyclic_order():
    boxes = [(float(a), float(b)) for a, b in KRAWCZYK_THETA_BOXES]
    assert boundary_order_ok(tuple(boxes))


@pytest.mark.fast
def test_variable_roles_documented():
    # u1..u4 map to square vertices p1..p4 in F; boundary order is u1,u4,u2,u3 by theta.
    mids = [0.5 * (float(a) + float(b)) for a, b in KRAWCZYK_THETA_BOXES]
    assert mids[0] < mids[3] < mids[1] < mids[2]
