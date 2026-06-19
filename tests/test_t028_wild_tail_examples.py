"""T028 wild-tail example tests."""

import pytest

from squarepeg.residual_curves.wild_tail_examples import all_wild_tail_examples, t028_applicable


@pytest.mark.fast
def test_three_examples():
    ex = all_wild_tail_examples()
    assert len(ex) >= 3
    names = {e.name for e in ex}
    assert "canonical_double_spiral" in names
    assert "modified_inner_exponent" in names
    assert "infinite_comb_tail" in names


@pytest.mark.fast
def test_t028_corollary_applicable():
    eta0, ok = t028_applicable()
    assert eta0 > 0
    assert ok
