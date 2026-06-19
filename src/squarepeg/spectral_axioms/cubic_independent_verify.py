"""Independent SymPy verification of cubic countermodel (no import from cubic_countermodel)."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class SymbolicVerification:
    endpoints_ok: bool
    centered_ok: bool
    derivative_ok: bool
    lip_max: int
    H_factorization_ok: bool
    symmetry_ok: bool
    D_h_ok: bool
    D_plus_zero: bool


def verify_symbolically() -> SymbolicVerification:
    x, y, h = sp.symbols("x y h", real=True)
    g = 4 * x**3 - 6 * x**2 + 3 * x
    g_centered = 4 * (x - sp.Rational(1, 2)) ** 3 + sp.Rational(1, 2)

    endpoints_ok = sp.simplify(g.subs(x, 0)) == 0 and sp.simplify(g.subs(x, 1)) == 1
    centered_ok = sp.expand(g - g_centered) == 0

    gp = sp.diff(g, x)
    gp_fact = 3 * (2 * x - 1) ** 2
    derivative_ok = sp.expand(gp - gp_fact) == 0

    # max on [0,1]: endpoints and critical point x=1/2
    lip_candidates = [gp.subs(x, 0), gp.subs(x, 1), gp.subs(x, sp.Rational(1, 2))]
    lip_max = max(int(sp.simplify(c)) for c in lip_candidates)

    H = g.subs(x, x) + g.subs(x, y) - g.subs(x, x + y)
    H = sp.simplify(g + g.subs(x, y) - g.subs(x, x + y))
    H_fact = 12 * x * y * (1 - x - y)
    H_factorization_ok = sp.expand(H - H_fact) == 0

    symmetry_ok = sp.expand(g.subs(x, 1 - x) - (1 - g)) == 0

    half = sp.Rational(1, 2)
    D_h_expr = sp.simplify(
        (g.subs(x, half + h) - g.subs(x, half - h)) / (2 * h)
    )
    D_h_ok = sp.expand(D_h_expr - 4 * h**2) == 0

    D_plus = sp.limit(D_h_expr, h, 0, dir="+")
    D_plus_zero = D_plus == 0

    return SymbolicVerification(
        endpoints_ok=bool(endpoints_ok),
        centered_ok=bool(centered_ok),
        derivative_ok=bool(derivative_ok),
        lip_max=lip_max,
        H_factorization_ok=bool(H_factorization_ok),
        symmetry_ok=bool(symmetry_ok),
        D_h_ok=bool(D_h_ok),
        D_plus_zero=bool(D_plus_zero),
    )


def compare_with_rational(rational_facts: dict) -> bool:
    sym = verify_symbolically()
    return (
        sym.endpoints_ok == rational_facts["endpoints_ok"]
        and sym.centered_ok == rational_facts["centered_ok"]
        and sym.derivative_ok == rational_facts["derivative_factorization_ok"]
        and sym.lip_max == int(rational_facts["lip_constant"])
        and sym.H_factorization_ok == rational_facts["subadditivity_factorization_ok"]
        and sym.symmetry_ok == rational_facts["symmetry_ok"]
        and sym.D_h_ok == rational_facts["D_h_formula_ok"]
        and sym.D_plus_zero
    )
