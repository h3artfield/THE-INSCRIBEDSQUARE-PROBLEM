"""Tests for exact square branch literal stability."""

import pytest

from squarepeg.residual_curves.truncation_audit import (
    MACRO_BRANCH_EDGES,
    MACRO_BRANCH_PARAMS,
    certificates_identical,
    macro_square_certificate,
)


@pytest.mark.fast
def test_macro_branch_edges_are_0350_not_4n1():
    cert = macro_square_certificate(5)
    assert cert is not None
    assert cert.edge_indices == (0, 3, 5, 0)
    assert cert.edge_indices != (0, 3, 5, 21)


@pytest.mark.fast
def test_first_three_params_literal_identical():
    for n in (3, 4, 5):
        cert = macro_square_certificate(n)
        assert cert is not None
        assert cert.edge_parameters[:3] == MACRO_BRANCH_PARAMS[:3]


@pytest.mark.fast
def test_vertices_and_side_literal_identical():
    base = macro_square_certificate(3)
    assert base is not None
    for n in (4, 5):
        cert = macro_square_certificate(n)
        assert cert is not None
        assert certificates_identical(base, cert)


@pytest.mark.fast
def test_all_supporting_edges_outer_arm():
    cert = macro_square_certificate(6)
    assert cert is not None
    assert all(d.kind == "outer_arm" for d in cert.edge_descriptors)


@pytest.mark.slow
def test_literal_stability_n8():
    base = macro_square_certificate(3)
    cert = macro_square_certificate(8)
    assert cert is not None
    assert certificates_identical(base, cert)
