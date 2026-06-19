"""Independent SymPy vs rational cubic verification agreement."""

import pytest

from squarepeg.spectral_axioms.cubic_countermodel import verify_all_identities
from squarepeg.spectral_axioms.cubic_independent_verify import (
    compare_with_rational,
    verify_symbolically,
)


@pytest.mark.fast
def test_symbolic_verification():
    sym = verify_symbolically()
    assert sym.endpoints_ok
    assert sym.centered_ok
    assert sym.derivative_ok
    assert sym.lip_max == 3
    assert sym.H_factorization_ok
    assert sym.symmetry_ok
    assert sym.D_h_ok
    assert sym.D_plus_zero


@pytest.mark.fast
def test_dual_implementations_agree():
    facts = verify_all_identities()
    rational_dict = {
        "endpoints_ok": facts.endpoints_ok,
        "centered_ok": facts.centered_form_ok,
        "derivative_factorization_ok": facts.derivative_factorization_ok,
        "lip_constant": facts.lip_constant,
        "subadditivity_factorization_ok": facts.subadditivity_factorization_ok,
        "symmetry_ok": facts.symmetry_ok,
        "D_h_formula_ok": facts.D_h_formula_ok,
    }
    assert compare_with_rational(rational_dict)
