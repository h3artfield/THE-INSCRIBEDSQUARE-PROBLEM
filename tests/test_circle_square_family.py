"""Circle and family stress tests."""

import pytest

from squarepeg.robust_degree.normal_degree import normal_index_circle, t038_statement
from squarepeg.robust_degree.square_family import (
    audit_circle_stress_test,
    circle_square_family,
    product_box_boundary_hit,
)


@pytest.mark.fast
def test_circle_family_parametrization():
    fam = circle_square_family()
    u = fam.parametrization(0.0)
    assert len(u) == 4


@pytest.mark.fast
def test_circle_no_protected_product_box():
    verdict, mb = audit_circle_stress_test()
    assert verdict == "CIRCLE_HAS_NO_PROTECTED_PRODUCT_BOX"
    assert mb.family.dim == 1


@pytest.mark.fast
def test_normal_index_circle():
    cert = normal_index_circle()
    assert cert.family_dim == 1
    assert cert.use_mod2


@pytest.mark.fast
def test_t038_conjectural():
    assert "CONJECTURAL" in t038_statement()
